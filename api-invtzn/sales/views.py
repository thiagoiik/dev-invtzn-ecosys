from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def _get_user_role(self):
        try:
            from profiles.models import UserProfile
            profile = UserProfile.objects.get(remote_auth_id=self.request.user.id)
            return profile.custom_role
        except Exception:
            return 'CLIENT'

    def get_queryset(self):
        # ADMIN y VENDOR ven todas las ventas
        from profiles.models import UserProfile
        role = self._get_user_role()
        if role in [UserProfile.Role.ADMIN, UserProfile.Role.VENDOR]:
            return Order.objects.all().order_by('-created_at')
            
        return Order.objects.filter(user=self.request.user.id).order_by('-created_at')

    def perform_create(self, serializer):
        from profiles.models import UserProfile
        role = self._get_user_role()
        
        # Si es VENDOR/ADMIN y viene un user en la request, se lo asignamos
        if role in [UserProfile.Role.ADMIN, UserProfile.Role.VENDOR] and 'user' in self.request.data:
            serializer.save() # El serializer usará el user enviado
        else:
            # Forzamos al usuario actual
            serializer.save(user=self.request.user.id)
