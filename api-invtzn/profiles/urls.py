from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet

router = DefaultRouter()
# Registramos el viewset. No requiere una URL base profunda porque usaremos la acción @action
router.register(r'profiles', UserProfileViewSet, basename='profile')

urlpatterns = [
    path('test/', lambda r: HttpResponse("OK")), # Importa HttpResponse de django.http
    path('', include(router.urls)),
]