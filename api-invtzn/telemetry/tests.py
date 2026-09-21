import pytest
from rest_framework.test import APIClient
from unittest.mock import patch, MagicMock
from telemetry.models import SessionRecording
from profiles.models import UserProfile, CommunicationLog
from telemetry.tasks import save_rrweb_session_task

pytestmark = pytest.mark.django_db

def test_record_session_view_requires_auth():
    client = APIClient()
    response = client.post('/api/v1/telemetry/record-session/', {})
    assert response.status_code == 403

@patch('telemetry.views.save_rrweb_session_task.delay')
def test_record_session_view_success(mock_delay):
    client = APIClient()
    user = UserProfile.objects.create(remote_auth_id=1, custom_role='CLIENT')
    client.force_authenticate(user=user)
    
    payload = {
        'events': [{'type': 1}],
        'window_width': 1920,
        'window_height': 1080
    }
    response = client.post('/api/v1/telemetry/record-session/', payload, format='json')
    
    assert response.status_code == 202
    assert response.data['status'] == "Grabación de sesión encolada con éxito."
    mock_delay.assert_called_once()
    
    # Verify the arguments passed to celery
    _, kwargs = mock_delay.call_args
    assert kwargs['user_id'] == user.remote_auth_id
    assert kwargs['role'] == 'CLIENT'
    assert kwargs['window_width'] == 1920

def test_record_session_view_missing_events():
    client = APIClient()
    user = UserProfile.objects.create(remote_auth_id=1, custom_role='CLIENT')
    client.force_authenticate(user=user)
    
    response = client.post('/api/v1/telemetry/record-session/', {'window_width': 1920}, format='json')
    assert response.status_code == 400
    assert "error" in response.data

@patch('telemetry.tasks.SessionRecording.objects.create')
def test_celery_save_rrweb_session_task(mock_create):
    mock_recording = MagicMock()
    mock_recording.id = 999
    mock_create.return_value = mock_recording
    
    admin_user = UserProfile.objects.create(remote_auth_id=99, custom_role='ADMIN')
    client_user = UserProfile.objects.create(remote_auth_id=5, custom_role='CLIENT')
    
    result = save_rrweb_session_task(
        user_id=5,
        role='CLIENT',
        environment='sandbox',
        user_agent='TestAgent',
        window_width=100,
        window_height=100,
        events_payload=[{"type": 4}],
        error_message="Test Error"
    )
    
    assert result is True
    mock_create.assert_called_once()
    
    admin_logs = CommunicationLog.objects.filter(user=admin_user)
    assert admin_logs.count() == 1
    assert "Auto-Crash: Test Error" in admin_logs.first().subject
    
    client_logs = CommunicationLog.objects.filter(user=client_user)
    assert client_logs.count() == 1
    assert "Hemos recibido tu reporte de error" in client_logs.first().subject

@patch('telemetry.views.SessionRecordingViewSet.get_queryset')
def test_session_recording_viewset_list(mock_get_queryset):
    # Usar instancia de modelo en memoria para evitar el RecursionError de MagicMock
    mock_instance = SessionRecording(
        id=1, user_id=99, role='ADMIN', environment='sandbox', window_width=1920, window_height=1080
    )
    mock_get_queryset.return_value = [mock_instance]

    client = APIClient()
    user = UserProfile.objects.create(remote_auth_id=99, custom_role='ADMIN', full_name="Admin Test")
    client.force_authenticate(user=user)
    
    response = client.get('/api/v1/telemetry/sessions/')
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['user_name'] == "Admin Test"

@patch('telemetry.views.SessionRecording.objects.all')
@patch('telemetry.views.SessionRecordingViewSet.get_object')
def test_session_recording_viewset_delete_cascade(mock_get_object, mock_all):
    mock_recording = MagicMock()
    mock_recording.id = 777
    mock_get_object.return_value = mock_recording
    
    client = APIClient()
    user = UserProfile.objects.create(remote_auth_id=99, custom_role='ADMIN')
    client.force_authenticate(user=user)
    
    CommunicationLog.objects.create(
        user=user,
        channel=CommunicationLog.Channel.SYSTEM,
        subject=f"Nuevo reporte manual en Sandbox (Grabación ID: {mock_recording.id})"
    )
    CommunicationLog.objects.create(
        user=user,
        channel=CommunicationLog.Channel.SYSTEM,
        subject=f"✅ Hemos recibido tu reporte de error (ID: {mock_recording.id}). ¡Gracias por ayudarnos a mejorar!"
    )
    
    assert CommunicationLog.objects.count() == 2
    
    response = client.delete(f'/api/v1/telemetry/sessions/{mock_recording.id}/')
    assert response.status_code == 204
    
    mock_recording.delete.assert_called_once()
    assert CommunicationLog.objects.count() == 0
