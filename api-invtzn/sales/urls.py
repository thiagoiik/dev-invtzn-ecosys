from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, CashSessionViewSet, CommissionViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'cash-sessions', CashSessionViewSet, basename='cash-session')
router.register(r'commissions', CommissionViewSet, basename='commission')

urlpatterns = [
    path('', include(router.urls)),
]
