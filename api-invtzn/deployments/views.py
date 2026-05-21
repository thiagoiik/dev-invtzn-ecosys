from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Deployment
from .serializers import DeploymentSerializer

class DeploymentViewSet(viewsets.ModelViewSet):
    serializer_class = DeploymentSerializer
    
    permission_classes = [AllowAny]
    
    def get_permissions(self):
        if self.action in ['create', 'public_by_slug', 'public_rsvp_by_slug', 'public_metric_by_slug', 'open_graph']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        from profiles.models import UserProfile
        from django.db import models
        try:
            profile = UserProfile.objects.get(remote_auth_id=self.request.user.id)
            if profile.custom_role in [UserProfile.Role.ADMIN, UserProfile.Role.DESIGNER]:
                return Deployment.objects.all().order_by('-created_at')
            if profile.custom_role == UserProfile.Role.VENDOR:
                return Deployment.objects.filter(models.Q(user=self.request.user.id) | models.Q(vendor_id=self.request.user.id)).order_by('-created_at')
        except Exception:
            pass
            
        # Usuarios normales solo ven las suyas
        return Deployment.objects.filter(user=self.request.user.id).order_by('-created_at')

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        
        # Si es una petición segura (GET, HEAD, OPTIONS), ya lo filtró get_queryset
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return

        # Si el usuario es dueño, puede editar (cast a str para evitar errores de tipo int vs str)
        if str(obj.user) == str(request.user.id):
            return

        # Si no es dueño, revisamos si es ADMIN o DESIGNER
        from profiles.models import UserProfile
        from rest_framework.exceptions import PermissionDenied
        try:
            profile = UserProfile.objects.get(remote_auth_id=request.user.id)
            # VENDEDORES no pueden editar diseño, solo ver.
            if profile.custom_role in [UserProfile.Role.ADMIN, UserProfile.Role.DESIGNER]:
                return
        except Exception:
            pass
            
        raise PermissionDenied("No tienes permisos de diseñador para modificar esta invitación.")

    def perform_create(self, serializer):
        from profiles.models import UserProfile
        user_id = self.request.user.id if self.request.user.is_authenticated else None
        
        # Si es anónimo, forzamos DRAFT y is_paid=False
        if not user_id:
            serializer.save(
                user=None, 
                status=Deployment.StatusChoices.DRAFT,
                is_paid=False
            )
            return

        try:
            profile = UserProfile.objects.get(remote_auth_id=user_id)
            if profile.custom_role in [UserProfile.Role.ADMIN, UserProfile.Role.VENDOR] and 'user' in self.request.data:
                serializer.save(vendor_id=user_id)
                return
        except Exception:
            pass
            
        serializer.save(user=user_id)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny], url_path='slug/(?P<slug>[^/.]+)')
    def public_by_slug(self, request, slug=None):
        deployment = get_object_or_404(Deployment, slug=slug)
        # Solo devolvemos datos necesarios para el engine (no datos sensibles del usuario)
        return Response({
            'id': deployment.id,
            'status': deployment.status,
            'custom_data': deployment.custom_data,
            'slug': deployment.slug,
            'product_type': deployment.product.product_type
        })

    @action(detail=False, methods=['post'], permission_classes=[AllowAny], url_path='slug/(?P<slug>[^/.]+)/rsvp')
    def public_rsvp_by_slug(self, request, slug=None):
        deployment = get_object_or_404(Deployment, slug=slug)
        
        full_name = request.data.get('full_name')
        attending = request.data.get('attending')
        
        if not full_name:
            return Response({'error': 'El nombre completo es requerido'}, status=400)
            
        # Convert attending to boolean if it's a string
        is_attending = True
        if str(attending).lower() in ['false', 'no', '0']:
            is_attending = False

        from .models import Guest
        guest = Guest.objects.create(
            deployment=deployment,
            full_name=full_name,
            attending=is_attending
        )
        
        return Response({'success': 'Confirmación recibida', 'guest_id': guest.id})

    @action(detail=False, methods=['post'], permission_classes=[AllowAny], url_path='slug/(?P<slug>[^/.]+)/metric')
    def public_metric_by_slug(self, request, slug=None):
        deployment = get_object_or_404(Deployment, slug=slug)
        metric_type = request.data.get('metric_type', 'VISIT')
        
        # Parse client IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')

        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        # Geolocation logic (non-blocking, fast timeout fallback)
        city = 'Desconocido'
        country = 'Desconocido'
        
        # If IP is loopback or private range
        if ip in ['127.0.0.1', 'localhost', '::1', None] or ip.startswith('192.168.') or ip.startswith('10.'):
            city = 'Localhost'
            country = 'México'
        else:
            try:
                import requests
                # Use a fast timeout (e.g. 1.0s) so it doesn't block the request if service is slow
                geo_res = requests.get(f"http://ip-api.com/json/{ip}", timeout=1.0).json()
                if geo_res.get('status') == 'success':
                    city = geo_res.get('city', 'Desconocido')
                    country = geo_res.get('country', 'Desconocido')
            except Exception:
                pass

        from .models import DeploymentMetric
        metric = DeploymentMetric.objects.create(
            deployment=deployment,
            metric_type=metric_type,
            ip_address=ip,
            user_agent=user_agent[:500] if user_agent else '',
            city=city,
            country=country
        )
        
        return Response({
            'success': 'Métrica registrada',
            'city': city,
            'country': country
        })

    @action(detail=False, methods=['get'], permission_classes=[AllowAny], url_path='og/(?P<slug>[^/.]+)')
    def open_graph(self, request, slug=None):
        from django.http import HttpResponse
        
        deployment = get_object_or_404(Deployment, slug=slug)
        custom_data = deployment.custom_data or {}
        
        is_paid = deployment.is_paid
        
        title = "Te invitamos a nuestro evento especial"
        description = "Acompáñanos en este día tan importante. ¡Haz clic para ver todos los detalles!"
        
        host = request.META.get('HTTP_X_FORWARDED_HOST') or request.get_host()
        protocol = "https" if "localhost" not in host and "127.0.0.1" not in host else "http"
        base_url = f"{protocol}://{host}"
        
        image_url = f"{base_url}/static/deployments/og-free-banner.png"
        
        if is_paid:
            title = custom_data.get('og_title')
            description = custom_data.get('og_description')
            image_url = custom_data.get('og_image')
            
            if not title:
                cover_config = {}
                if isinstance(custom_data.get('blocks'), list):
                    for block in custom_data['blocks']:
                        if block.get('type') == 'CoverBlock':
                            cover_config = block.get('config', {})
                            break
                else:
                    cover_config = custom_data.get('cover', {})
                
                title = cover_config.get('title') or custom_data.get('event_title') or f"Invitación de {deployment.slug}"
                
            if not description:
                cover_config = {}
                if isinstance(custom_data.get('blocks'), list):
                    for block in custom_data['blocks']:
                        if block.get('type') == 'CoverBlock':
                            cover_config = block.get('config', {})
                            break
                else:
                    cover_config = custom_data.get('cover', {})
                
                description = cover_config.get('subtitle') or custom_data.get('event_description') or "¡Te invitamos a celebrar con nosotros!"
            
            if not image_url:
                cover_config = {}
                if isinstance(custom_data.get('blocks'), list):
                    for block in custom_data['blocks']:
                        if block.get('type') == 'CoverBlock':
                            cover_config = block.get('config', {})
                            break
                else:
                    cover_config = custom_data.get('cover', {})
                
                image_url = cover_config.get('coverPhoto') or f"{base_url}/static/deployments/og-premium-card.png"
        else:
            cover_config = {}
            if isinstance(custom_data.get('blocks'), list):
                for block in custom_data['blocks']:
                    if block.get('type') == 'CoverBlock':
                        cover_config = block.get('config', {})
                        break
            else:
                cover_config = custom_data.get('cover', {})
            
            event_title = cover_config.get('title') or custom_data.get('event_title') or "Boda Especial"
            title = f"Invitación: {event_title}"
            description = "Crea tus propias invitaciones digitales interactivas premium en Invitazyon.online"
        
        if image_url and not image_url.startswith('http://') and not image_url.startswith('https://'):
            if image_url.startswith('/'):
                image_url = f"{base_url}{image_url}"
            else:
                image_url = f"{base_url}/{image_url}"

        canonical_url = f"{base_url}/i/{slug}"
        
        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:image" content="{image_url}">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:type" content="article">
    <meta property="og:site_name" content="Invitazyon">
    
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="{image_url}">
    
    <meta name="robots" content="noindex, nofollow">
</head>
<body>
    <h1>{title}</h1>
    <p>{description}</p>
    <img src="{image_url}" alt="Banner de Invitación">
</body>
</html>"""
        return HttpResponse(html, content_type="text/html; charset=utf-8")
