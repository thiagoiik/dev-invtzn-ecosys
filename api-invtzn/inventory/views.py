from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product, Store
from .serializers import ProductSerializer, StoreSerializer
from integrations.stripe_provider import StripeProvider

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    # La tienda es pública (para ver), pero solo el Admin crea productos
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class StoreViewSet(viewsets.ModelViewSet):
    serializer_class = StoreSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        from profiles.models import UserProfile
        user_id = self.request.user.id
        try:
            profile = UserProfile.objects.get(remote_auth_id=user_id)
            if profile.custom_role == UserProfile.Role.ADMIN:
                return Store.objects.all()
            if profile.custom_role == UserProfile.Role.FRANCHISEE:
                return Store.objects.filter(owner=profile)
            if profile.custom_role == UserProfile.Role.MANAGER:
                # El gerente ve la tienda a la que está asignado
                if profile.assigned_store:
                    return Store.objects.filter(id=profile.assigned_store.id)
        except UserProfile.DoesNotExist:
            pass
        return Store.objects.none()

    def perform_create(self, serializer):
        from profiles.models import UserProfile
        profile = UserProfile.objects.get(remote_auth_id=self.request.user.id)
        # Si un Franquiciatario crea una tienda, él es el dueño automáticamente
        if profile.custom_role == UserProfile.Role.FRANCHISEE:
            serializer.save(owner=profile)
        else:
            serializer.save()

    @action(detail=True, methods=['post'], url_path='stripe-onboarding')
    def onboarding_link(self, request, pk=None):
        store = self.get_object()
        return_url = request.data.get('return_url', 'http://localhost:5173/workspace/stores')
        refresh_url = request.data.get('refresh_url', 'http://localhost:5173/workspace/stores')
        
        try:
            url = StripeProvider.create_onboarding_link(store, return_url, refresh_url)
            return Response({'url': url})
        except Exception as e:
            print(f"DEBUG STRIPE ERROR: {e}")
            return Response({'error': str(e)}, status=400)

    @action(detail=True, methods=['get'], url_path='stripe-verify')
    def verify_onboarding(self, request, pk=None):
        store = self.get_object()
        is_complete = StripeProvider.check_onboarding_status(store)
        return Response({
            'stripe_onboarding_completed': is_complete,
            'stripe_account_id': store.stripe_account_id
        })