import uuid
import logging
import contextvars
from django.utils.deprecation import MiddlewareMixin

_trace_id_ctx = contextvars.ContextVar('auth_trace_id', default='-')
_user_id_ctx = contextvars.ContextVar('auth_user_id', default='-')


def get_current_trace_id():
    return _trace_id_ctx.get()


def get_current_user_id():
    return _user_id_ctx.get()


class TraceCorrelationMiddleware(MiddlewareMixin):
    """
    Middleware que propaga el Correlation/Trace ID en auth-service.
    Garantiza trazabilidad unificada entre auth-service, gateway y api-invtzn.
    """

    def process_request(self, request):
        trace_id = (
            request.headers.get('X-Correlation-ID')
            or request.headers.get('X-Trace-ID')
            or request.headers.get('X-Request-ID')
            or uuid.uuid4().hex[:12]
        )
        _trace_id_ctx.set(trace_id)
        request.trace_id = trace_id

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
    def filter(self, record):
        if not hasattr(record, 'trace_id'):
            record.trace_id = get_current_trace_id()
        if not hasattr(record, 'user_id'):
            record.user_id = get_current_user_id()
        return True
