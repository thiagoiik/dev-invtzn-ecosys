from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReconciliationViewSet, StripeWebhookView

router = DefaultRouter()
router.register(r'integrations', ReconciliationViewSet, basename='reconciliation')

urlpatterns = [
    path('stripe-webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),
    path('', include(router.urls)),
]
