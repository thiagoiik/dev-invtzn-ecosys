from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Deployment
from .serializers import DeploymentSerializer

class DeploymentViewSet(viewsets.ModelViewSet):
    serializer_class = DeploymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Cada usuario solo puede ver y editar sus propios deployments
        return Deployment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny], url_path='slug/(?P<slug>[^/.]+)')
    def public_by_slug(self, request, slug=None):
        deployment = get_object_or_404(Deployment, slug=slug)
        # Solo devolvemos datos necesarios para el engine (no datos sensibles del usuario)
        return Response({
            'status': deployment.status,
            'custom_data': deployment.custom_data,
            'slug': deployment.slug,
            'product_type': deployment.product.product_type
        })
