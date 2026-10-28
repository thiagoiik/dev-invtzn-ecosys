from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, CashSessionViewSet, CommissionViewSet, CouponViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'cash-sessions', CashSessionViewSet, basename='cash-session')
router.register(r'commissions', CommissionViewSet, basename='commission')
router.register(r'coupons', CouponViewSet, basename='coupon')

urlpatterns = [
    path('', include(router.urls)),
]
