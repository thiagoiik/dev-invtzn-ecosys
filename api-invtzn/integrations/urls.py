from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReconciliationViewSet, StripeWebhookView, WebhookLogViewSet

router = DefaultRouter()
router.register(r'integrations', ReconciliationViewSet, basename='reconciliation')
router.register(r'webhook-logs', WebhookLogViewSet, basename='webhook-logs')

urlpatterns = [
    path('stripe-webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),
    path('', include(router.urls)),
]
