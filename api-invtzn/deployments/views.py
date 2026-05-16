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
        if self.action == 'create':
            return [AllowAny()]
        # Para ver slugs públicos
        if self.action == 'public_by_slug':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        from profiles.models import UserProfile
        from django.db import models
        try:
            profile = UserProfile.objects.get(remote_auth_id=self.request.user.id)
            if profile.custom_role == UserProfile.Role.ADMIN:
                return Deployment.objects.all().order_by('-created_at')
            if profile.custom_role in [UserProfile.Role.VENDOR, UserProfile.Role.DESIGNER]:
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
