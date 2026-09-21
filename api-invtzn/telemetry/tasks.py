import logging
from celery import shared_task
from .models import SessionRecording

logger = logging.getLogger(__name__)

@shared_task(name='telemetry.tasks.save_rrweb_session_task')
def save_rrweb_session_task(user_id, role, environment, user_agent, window_width, window_height, events_payload):
    try:
        recording = SessionRecording.objects.create(
            user_id=user_id,
            role=role,
            environment=environment,
            user_agent=user_agent,
            window_width=window_width,
            window_height=window_height,
            events_payload=events_payload
        )
        return True
    except Exception as e:
        logger.error(f"Error al guardar SessionRecording de rrweb: {e}")
        return False
