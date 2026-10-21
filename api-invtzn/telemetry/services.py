import logging
from .models import SystemLog
from invtzn_core.middleware import get_current_trace_id

audit_logger = logging.getLogger('audit.activity')


def record_activity(
    log_type,
    message,
    user=None,
    user_id=None,
    username=None,
    metadata=None,
    ip_address=None
):
    """
    Servicio central de auditoría y telemetría de acciones:
    1. Persiste el registro en la base de datos 'telemetry_db' (aislada del core transaccional).
    2. Emite simultáneamente un log JSON estructurado por stdout (capturado por Promtail y almacenado en Grafana Loki).
    """
    metadata = metadata.copy() if metadata else {}

    # Resolver user_id y username de forma agnóstica
    resolved_user_id = user_id
    resolved_username = username

    if user is not None:
        if hasattr(user, 'id'):
            resolved_user_id = user.id
        if getattr(user, 'email', None):
            resolved_username = user.email
        elif getattr(user, 'username', None):
            resolved_username = user.username
        elif getattr(user, 'full_name', None):
            resolved_username = user.full_name

    trace_id = get_current_trace_id()
    if trace_id and trace_id != '-':
        metadata['trace_id'] = trace_id
    if ip_address:
        metadata['ip_address'] = ip_address

    # 1. Guardar en base de datos separada (telemetry_db via TelemetryRouter)
    try:
        system_log = SystemLog.objects.create(
            log_type=log_type,
            message=message,
            user_id=resolved_user_id,
            username=resolved_username,
            metadata=metadata
        )
    except Exception as e:
        audit_logger.error(
            f"Fallo al persistir en telemetry_db: {str(e)}",
            extra={'trace_id': trace_id, 'log_type': log_type}
        )
        system_log = None

    # 2. Emitir log estructurado hacia Promtail -> Loki
    audit_logger.info(
        message,
        extra={
            'event': 'SYSTEM_AUDIT',
            'log_type': log_type,
            'user_id': resolved_user_id,
            'username': resolved_username,
            'trace_id': trace_id,
            'audit_metadata': metadata
        }
    )

    return system_log
