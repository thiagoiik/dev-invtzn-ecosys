from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecordSessionView, SessionRecordingViewSet

router = DefaultRouter()
router.register(r'sessions', SessionRecordingViewSet, basename='session-recording')

urlpatterns = [
    path('record-session/', RecordSessionView.as_view(), name='record-session'),
    path('', include(router.urls)),
]
