from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
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
