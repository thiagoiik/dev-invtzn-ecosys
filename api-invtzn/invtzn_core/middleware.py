import uuid
import logging
import contextvars
from django.utils.deprecation import MiddlewareMixin

# ContextVars para almacenar el identificador de rastreo de manera segura por hilo/tarea async
_trace_id_ctx = contextvars.ContextVar('trace_id', default='-')
_user_id_ctx = contextvars.ContextVar('user_id', default='-')


def get_current_trace_id():
    """Retorna el Correlation/Trace ID de la petición activa o '-' si está fuera de contexto."""
    return _trace_id_ctx.get()


def get_current_user_id():
    """Retorna el ID de usuario activo o '-' si es anónimo/fuera de contexto."""
    return _user_id_ctx.get()


class TraceCorrelationMiddleware(MiddlewareMixin):
    """
    Middleware que captura o genera un Trace/Correlation ID para cada petición HTTP.
    Inyecta el identificador en los registros de log y en los headers de respuesta (X-Correlation-ID).
    """

    def process_request(self, request):
        # 1. Leer Trace ID desde los encabezados entrantes (NGINX / Gateway / Microservicio)
        trace_id = (
            request.headers.get('X-Correlation-ID')
            or request.headers.get('X-Trace-ID')
            or request.headers.get('X-Request-ID')
            or uuid.uuid4().hex[:12]
        )
        _trace_id_ctx.set(trace_id)
        request.trace_id = trace_id

        # 2. Capturar user_id si ya está autenticado
        user = getattr(request, 'user', None)
        if user and getattr(user, 'is_authenticated', False):
            _user_id_ctx.set(str(user.id))
        else:
            _user_id_ctx.set('anonymous')

    def process_response(self, request, response):
        trace_id = getattr(request, 'trace_id', None) or _trace_id_ctx.get()
        if trace_id and trace_id != '-':
            response['X-Correlation-ID'] = trace_id
        return response


class CorrelationLogFilter(logging.Filter):
    """
    Filtro de Logging que inyecta trace_id y user_id en cada registro emitido.
    Permite que los formatters (JSON o texto) incluyan automáticamente estos metadatos.
    """

    def filter(self, record):
        if not hasattr(record, 'trace_id'):
            record.trace_id = get_current_trace_id()
        if not hasattr(record, 'user_id'):
            record.user_id = get_current_user_id()
        return True
