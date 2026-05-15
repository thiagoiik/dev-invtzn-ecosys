from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import UserProfile
from .serializers import UserProfileSerializer

class UserProfileViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        # Si el usuario es ADMIN, puede ver a todos los usuarios
        try:
            profile = UserProfile.objects.get(remote_auth_id=self.request.user.id)
            if profile.custom_role == UserProfile.Role.ADMIN:
                return UserProfile.objects.all()
        except UserProfile.DoesNotExist:
            pass
        # Si no, solo puede verse a sí mismo
        return UserProfile.objects.filter(remote_auth_id=self.request.user.id)

    # Creamos un endpoint personalizado: /api/v1/profiles/me/
    @action(detail=False, methods=['get', 'post', 'patch'])
    def me(self, request):
        # request.user.id viene directamente del JWT decodificado en authentication.py
        user_id = request.user.id
        
        # Sincronizamos el full_name si viene en el body
        full_name = request.data.get('full_name')
        
        # Buscamos el perfil. Si no existe, lo creamos.
        profile, created = UserProfile.objects.get_or_create(
            remote_auth_id=user_id,
            defaults={
                'custom_role': UserProfile.Role.CLIENT,
                'full_name': full_name or ""
            }
        )

        # Si ya existe pero enviamos un nombre nuevo, lo actualizamos (Sincronización)
        if not created and full_name and profile.full_name != full_name:
            profile.full_name = full_name
            profile.save()

        if request.method in ['GET', 'POST']:
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
            
        elif request.method == 'PATCH':
            # Permitimos que el usuario actualice su teléfono, por ejemplo
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        # Permite a VENDOR y ADMIN buscar un usuario por remote_auth_id sin exponer toda la base de datos
        try:
            profile = UserProfile.objects.get(remote_auth_id=request.user.id)
            if profile.custom_role not in [UserProfile.Role.ADMIN, UserProfile.Role.VENDOR]:
                return Response({'error': 'No tienes permisos.'}, status=403)
        except UserProfile.DoesNotExist:
            return Response({'error': 'No tienes perfil asignado.'}, status=403)

        user_id = request.query_params.get('remote_auth_id')
        if not user_id:
            return Response({'error': 'remote_auth_id es requerido'}, status=400)
            
        try:
            user_profile = UserProfile.objects.get(remote_auth_id=user_id)
            serializer = self.get_serializer(user_profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=404)

    @action(detail=True, methods=['patch'], url_path='change-role')
    def change_role(self, request, pk=None):
        # Solo administradores pueden cambiar roles
        try:
            admin_profile = UserProfile.objects.get(remote_auth_id=request.user.id)
            if admin_profile.custom_role != UserProfile.Role.ADMIN:
                return Response({'error': 'No tienes permisos de administrador.'}, status=403)
        except UserProfile.DoesNotExist:
            return Response({'error': 'No tienes perfil asignado.'}, status=403)

        user_to_promote = self.get_object()
        new_role = request.data.get('custom_role')
        
        if new_role not in dict(UserProfile.Role.choices):
            return Response({'error': 'Rol inválido.'}, status=400)
            
        user_to_promote.custom_role = new_role
        user_to_promote.save()
        
        return Response({'success': f'Rol cambiado a {new_role}'})