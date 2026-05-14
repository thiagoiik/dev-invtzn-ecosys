from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import UserProfile
from .serializers import UserProfileSerializer

class UserProfileViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        # Si el usuario es ADMIN o VENDOR, puede ver a todos los usuarios
        try:
            profile = UserProfile.objects.get(remote_auth_id=self.request.user.id)
            if profile.custom_role in [UserProfile.Role.ADMIN, UserProfile.Role.VENDOR]:
                return UserProfile.objects.all()
        except UserProfile.DoesNotExist:
            pass
        # Si no, solo puede verse a sí mismo
        return UserProfile.objects.filter(remote_auth_id=self.request.user.id)

    # Creamos un endpoint personalizado: /api/v1/profiles/me/
    @action(detail=False, methods=['get', 'patch'])
    def me(self, request):
        # request.user.id viene directamente del JWT decodificado en authentication.py
        user_id = request.user.id
        
        # MAGIA: Buscamos el perfil. Si no existe en esta DB, lo creamos asignándole rol CLIENT
        profile, created = UserProfile.objects.get_or_create(
            remote_auth_id=user_id,
            defaults={'custom_role': UserProfile.Role.CLIENT}
        )

        if request.method == 'GET':
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
            
        elif request.method == 'PATCH':
            # Permitimos que el usuario actualice su teléfono, por ejemplo
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)