from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, CashSession, Commission
from .serializers import OrderSerializer, CashSessionSerializer, CommissionSerializer
from profiles.models import UserProfile
from django.db import models

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def _get_user_profile(self):
        try:
            return UserProfile.objects.get(remote_auth_id=self.request.user.id)
        except UserProfile.DoesNotExist:
            return None

    def get_queryset(self):
        profile = self._get_user_profile()
        if not profile:
            return Order.objects.none()
            
        if profile.custom_role == UserProfile.Role.ADMIN:
            return Order.objects.all().order_by('-created_at')
        if profile.custom_role == UserProfile.Role.VENDOR:
            return Order.objects.filter(
                models.Q(user=self.request.user.id) | 
                models.Q(vendor_id=self.request.user.id)
            ).order_by('-created_at')
            
        return Order.objects.filter(user=self.request.user.id).order_by('-created_at')

    def perform_create(self, serializer):
        profile = self._get_user_profile()
        role = profile.custom_role if profile else UserProfile.Role.CLIENT
        
        # Valores por defecto
        save_kwargs = {}
        
        if role in [UserProfile.Role.ADMIN, UserProfile.Role.VENDOR]:
            # Si el Staff registra la orden para un cliente (Buscó al cliente en el POS)
            if 'user' in self.request.data:
                save_kwargs['vendor_id'] = self.request.user.id
                save_kwargs['origin'] = Order.OriginChoices.POS
                if profile and profile.assigned_store:
                    save_kwargs['store'] = profile.assigned_store
            else:
                # El staff compra para sí mismo (B2C flow siendo staff)
                save_kwargs['user'] = self.request.user.id
                save_kwargs['origin'] = Order.OriginChoices.ONLINE
        else:
            # Cliente normal comprando online
            save_kwargs['user'] = self.request.user.id
            save_kwargs['origin'] = Order.OriginChoices.ONLINE

        order = serializer.save(**save_kwargs)
        
        # Lógica de Comisiones: Solo si es POS y hay un vendedor diferente al cliente
        if order.origin == Order.OriginChoices.POS and order.vendor_id:
            if profile and profile.base_commission_rate > 0:
                commission_amount = (order.total_amount * profile.base_commission_rate) / 100
                Commission.objects.create(
                    order=order,
                    vendor_id=order.vendor_id,
                    amount=commission_amount,
                    percentage=profile.base_commission_rate
                )

class CashSessionViewSet(viewsets.ModelViewSet):
    serializer_class = CashSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        from profiles.models import UserProfile
        try:
            profile = UserProfile.objects.get(remote_auth_id=self.request.user.id)
            if profile.custom_role == UserProfile.Role.ADMIN:
                return CashSession.objects.all()
        except: pass
        return CashSession.objects.filter(user=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.id)

class CommissionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CommissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        from profiles.models import UserProfile
        try:
            profile = UserProfile.objects.get(remote_auth_id=self.request.user.id)
            if profile.custom_role == UserProfile.Role.ADMIN:
                return Commission.objects.all()
        except: pass
        return Commission.objects.filter(vendor_id=self.request.user.id)
