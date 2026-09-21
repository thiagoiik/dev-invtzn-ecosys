from django.urls import path
from .views import RecordSessionView

urlpatterns = [
    path('record-session/', RecordSessionView.as_view(), name='record-session'),
]
