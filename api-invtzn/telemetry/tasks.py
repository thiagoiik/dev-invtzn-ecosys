import logging
from celery import shared_task
from .models import SessionRecording
from profiles.models import UserProfile, CommunicationLog

logger = logging.getLogger(__name__)

@shared_task(name='telemetry.tasks.save_rrweb_session_task')
def save_rrweb_session_task(user_id, role, environment, user_agent, window_width, window_height, events_payload, error_message=''):
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
        
        # Generar asunto dinámico
        if error_message:
            subject_text = f"Auto-Crash: {error_message[:50]}... (Grabación ID: {recording.id})"
        else:
            subject_text = f"Nuevo reporte manual en Sandbox (Grabación ID: {recording.id})"

        # Notificar a todos los administradores (usando CommunicationLog)
        admins = UserProfile.objects.filter(custom_role=UserProfile.Role.ADMIN)
        for admin in admins:
            CommunicationLog.objects.create(
                user=admin,
                channel=CommunicationLog.Channel.SYSTEM,
                subject=subject_text
            )
            
        # Notificar de vuelta al usuario que lo envió
        if user_id:
            try:
                sender = UserProfile.objects.get(remote_auth_id=user_id)
                CommunicationLog.objects.create(
                    user=sender,
                    channel=CommunicationLog.Channel.SYSTEM,
                    subject=f"✅ Hemos recibido tu reporte de error (ID: {recording.id}). ¡Gracias por ayudarnos a mejorar!"
                )
            except UserProfile.DoesNotExist:
                pass
            
        return True
    except Exception as e:
        logger.error(f"Error al guardar SessionRecording de rrweb: {e}")
        return False
