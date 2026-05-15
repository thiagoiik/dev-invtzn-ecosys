from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, StoreViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'stores', StoreViewSet, basename='store')

urlpatterns = [
    path('', include(router.urls)),
]