from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def _get_user_role(self):
        from profiles.models import UserProfile
        try:
            profile = UserProfile.objects.get(remote_auth_id=self.request.user.id)
            return profile.custom_role
        except UserProfile.DoesNotExist:
            return None

    def get_queryset(self):
        # ADMIN ve todo. VENDOR ve lo suyo y lo que vendió. CLIENT ve lo suyo.
        from profiles.models import UserProfile
        from django.db import models
        role = self._get_user_role()
        
        if role == UserProfile.Role.ADMIN:
            return Order.objects.all().order_by('-created_at')
        if role == UserProfile.Role.VENDOR:
            return Order.objects.filter(models.Q(user=self.request.user.id) | models.Q(vendor_id=self.request.user.id)).order_by('-created_at')
            
        return Order.objects.filter(user=self.request.user.id).order_by('-created_at')

    def perform_create(self, serializer):
        from profiles.models import UserProfile
        role = self._get_user_role()
        
        # Si es VENDOR/ADMIN y viene un user en la request, se lo asignamos
        if role in [UserProfile.Role.ADMIN, UserProfile.Role.VENDOR] and 'user' in self.request.data:
            serializer.save(vendor_id=self.request.user.id) # El serializer usará el user enviado pero registramos el vendor_id
        else:
            # Forzamos al usuario actual
            serializer.save(user=self.request.user.id)
