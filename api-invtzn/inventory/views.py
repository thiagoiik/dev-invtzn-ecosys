from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    # La tienda es pública (para ver), pero solo el Admin crea productos
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]