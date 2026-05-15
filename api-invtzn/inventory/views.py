from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Product, Store
from .serializers import ProductSerializer, StoreSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    # La tienda es pública (para ver), pero solo el Admin crea productos
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.filter(is_active=True)
    serializer_class = StoreSerializer
    permission_classes = [permissions.IsAuthenticated]