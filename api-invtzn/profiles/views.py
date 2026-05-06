from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import UserProfile
from .serializers import UserProfileSerializer

class UserProfileViewSet(viewsets.GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

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