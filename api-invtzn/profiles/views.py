from rest_framework import viewsets, mixins, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import UserProfile, WalletLog, SiteReview, CommunicationLog
from .serializers import UserProfileSerializer, WalletLogSerializer, SiteReviewSerializer, CommunicationLogSerializer

class UserProfileViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserProfileSerializer
    lookup_field = 'remote_auth_id'

    def dispatch(self, request, *args, **kwargs):
        print(f"DEBUG DISPATCH: {request.method} {request.path}")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        try:
            profile = UserProfile.objects.get(remote_auth_id=self.request.user.id)
            if profile.custom_role == UserProfile.Role.ADMIN:
                return UserProfile.objects.all()
            
            if profile.custom_role == UserProfile.Role.FRANCHISEE:
                # El franquiciatario ve el personal de sus tiendas
                from inventory.models import Store
                owned_stores = Store.objects.filter(owner=profile)
                return UserProfile.objects.filter(assigned_store__in=owned_stores)
                
            if profile.custom_role == UserProfile.Role.MANAGER:
                # El gerente ve el personal de su tienda asignada
                if profile.assigned_store:
                    return UserProfile.objects.filter(assigned_store=profile.assigned_store)
                    
        except UserProfile.DoesNotExist:
            pass
        # Si no, solo puede verse a sí mismo
        return UserProfile.objects.filter(remote_auth_id=self.request.user.id)

    def partial_update(self, request, *args, **kwargs):
        print(f"DEBUG UPDATE PROFILE: {kwargs.get('remote_auth_id')} with data {request.data}")
        return super().partial_update(request, *args, **kwargs)

    # Creamos un endpoint personalizado: /api/v1/profiles/me/
    @action(detail=False, methods=['get', 'post', 'patch'])
    def me(self, request):
        user_id = request.user.id
        full_name = request.data.get('full_name')
        
        profile, created = UserProfile.objects.get_or_create(
            remote_auth_id=user_id,
            defaults={
                'custom_role': UserProfile.Role.CLIENT,
                'full_name': full_name or ""
            }
        )

        if not created and full_name and profile.full_name != full_name:
            profile.full_name = full_name
            profile.save()

        if request.method in ['GET', 'POST']:
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
            
        elif request.method == 'PATCH':
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        try:
            profile = UserProfile.objects.get(remote_auth_id=request.user.id)
            if profile.custom_role not in [UserProfile.Role.ADMIN, UserProfile.Role.VENDOR, UserProfile.Role.FRANCHISEE]:
                return Response({'error': 'No tienes permisos.'}, status=403)
        except UserProfile.DoesNotExist:
            return Response({'error': 'No tienes perfil asignado.'}, status=403)

        query = request.query_params.get('query')
        user_id = request.query_params.get('remote_auth_id')

        if query:
            from django.db.models import Q
            queryset = UserProfile.objects.filter(
                Q(full_name__icontains=query) |
                Q(phone_number__icontains=query) |
                Q(email__icontains=query)
            )
            if query.isdigit():
                queryset = queryset | UserProfile.objects.filter(remote_auth_id=int(query))
            
            serializer = self.get_serializer(queryset[:10], many=True)
            return Response(serializer.data)

        if not user_id:
            return Response({'error': 'Debe proporcionar query o remote_auth_id'}, status=400)
            
        try:
            user_profile = UserProfile.objects.get(remote_auth_id=user_id)
            serializer = self.get_serializer(user_profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=404)

    @action(detail=False, methods=['get'])
    def notifications(self, request):
        try:
            profile = UserProfile.objects.get(remote_auth_id=request.user.id)
        except UserProfile.DoesNotExist:
            return Response({'error': 'No tienes perfil asignado.'}, status=403)
            
        if profile.custom_role != UserProfile.Role.ADMIN:
            return Response([])
            
        import re
        from deployments.models import Deployment
        
        logs = CommunicationLog.objects.filter(
            user=profile,
            channel=CommunicationLog.Channel.SYSTEM
        ).order_by('-sent_at')[:100]
        
        filtered_notifications = []
        for log in logs:
            match = re.search(r'\(ID:\s*(\d+)\)', log.subject)
            if match:
                deployment_id = int(match.group(1))
                try:
                    deployment = Deployment.objects.get(id=deployment_id)
                    if deployment.status == Deployment.StatusChoices.DRAFT:
                        filtered_notifications.append(log)
                except Deployment.DoesNotExist:
                    pass
            else:
                filtered_notifications.append(log)
                
            if len(filtered_notifications) >= 20:
                break
                
        serializer = CommunicationLogSerializer(filtered_notifications, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], url_path='change-role')
    def change_role(self, request, remote_auth_id=None):
        print(f"DEBUG CHANGE ROLE: User {request.user.id} attempting to change profile {remote_auth_id}")
        try:
            current_user_profile = UserProfile.objects.get(remote_auth_id=request.user.id)
            print(f"DEBUG CHANGE ROLE: Current user role: {current_user_profile.custom_role}")
            is_admin = current_user_profile.custom_role == UserProfile.Role.ADMIN
            is_franchisee = current_user_profile.custom_role == UserProfile.Role.FRANCHISEE
            
            if not is_admin and not is_franchisee:
                return Response({'error': 'No tienes permisos para cambiar roles.'}, status=403)
        except UserProfile.DoesNotExist:
            return Response({'error': 'No tienes perfil asignado.'}, status=403)

        user_to_promote = self.get_object()
        new_role = request.data.get('custom_role')
        
        if new_role not in dict(UserProfile.Role.choices):
            return Response({'error': 'Rol inválido.'}, status=400)
            
        # Validar jerarquía
        if is_franchisee:
            # Un franquiciatario no puede crear un ADMIN
            if new_role == UserProfile.Role.ADMIN:
                return Response({'error': 'No puedes asignar rol de ADMIN.'}, status=403)
            # Debe ser personal de su tienda
            from inventory.models import Store
            if not Store.objects.filter(owner=current_user_profile, id=user_to_promote.assigned_store_id).exists():
                return Response({'error': 'El usuario no pertenece a tus sucursales.'}, status=403)

        user_to_promote.custom_role = new_role
        user_to_promote.save()
        
        return Response({'success': f'Rol cambiado a {new_role}'})

class WalletLogViewSet(viewsets.ModelViewSet):
    queryset = WalletLog.objects.all().order_by('-timestamp')
    serializer_class = WalletLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            profile = UserProfile.objects.get(remote_auth_id=self.request.user.id)
            if profile.custom_role == UserProfile.Role.ADMIN:
                return WalletLog.objects.all().order_by('-timestamp')
        except: pass
        return WalletLog.objects.filter(user__remote_auth_id=self.request.user.id).order_by('-timestamp')

class SiteReviewViewSet(viewsets.ModelViewSet):
    queryset = SiteReview.objects.all().order_by('-created_at')
    serializer_class = SiteReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            profile = UserProfile.objects.get(remote_auth_id=self.request.user.id)
        except UserProfile.DoesNotExist:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("El perfil de usuario no existe.")
        serializer.save(user=profile)

    def get_queryset(self):
        try:
            profile = UserProfile.objects.get(remote_auth_id=self.request.user.id)
            if profile.custom_role in [UserProfile.Role.ADMIN, UserProfile.Role.FRANCHISEE]:
                return SiteReview.objects.all().order_by('-created_at')
        except UserProfile.DoesNotExist:
            pass
        return SiteReview.objects.filter(user__remote_auth_id=self.request.user.id).order_by('-created_at')

    @action(detail=False, methods=['get'], url_path='public', permission_classes=[permissions.AllowAny])
    def public(self, request):
        approved_reviews = SiteReview.objects.filter(is_approved=True).order_by('-created_at')[:8]
        serializer = self.get_serializer(approved_reviews, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='toggle-approve')
    def toggle_approve(self, request, pk=None):
        try:
            current_profile = UserProfile.objects.get(remote_auth_id=request.user.id)
            if current_profile.custom_role not in [UserProfile.Role.ADMIN, UserProfile.Role.FRANCHISEE]:
                return Response({'error': 'No tienes permisos para moderar reseñas.'}, status=403)
        except UserProfile.DoesNotExist:
            return Response({'error': 'No tienes perfil asignado.'}, status=403)

        review = self.get_object()
        review.is_approved = not review.is_approved
        review.save()
        return Response({'success': f'Estado de aprobación cambiado a {review.is_approved}', 'is_approved': review.is_approved})