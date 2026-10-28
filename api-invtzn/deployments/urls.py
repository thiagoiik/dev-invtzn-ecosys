from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeploymentViewSet, SystemLogViewSet

router = DefaultRouter()
router.register(r'deployments', DeploymentViewSet, basename='deployment')
router.register(r'system-logs', SystemLogViewSet, basename='system-log')

urlpatterns = [
    path('', include(router.urls)),
]
