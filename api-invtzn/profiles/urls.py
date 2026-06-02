from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, WalletLogViewSet, SiteReviewViewSet

router = DefaultRouter()
# Registramos el viewset. No requiere una URL base profunda porque usaremos la acción @action
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'wallet-logs', WalletLogViewSet, basename='wallet-log')
router.register(r'reviews', SiteReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
]