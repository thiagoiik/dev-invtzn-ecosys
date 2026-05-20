from .base import *
import dj_database_url

# Validación obligatoria de seguridad en producción
SECRET_KEY = os.environ.get('AUTH_DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("CRÍTICO: La variable AUTH_DJANGO_SECRET_KEY debe estar configurada en entornos de producción.")

# Forzar DEBUG en False bajo cualquier circunstancia
DEBUG = False

ALLOWED_HOSTS = os.environ.get('AUTH_DJANGO_ALLOWED_HOSTS', '').split(',')
if not ALLOWED_HOSTS or ALLOWED_HOSTS == ['']:
    raise ValueError("CRÍTICO: La variable AUTH_DJANGO_ALLOWED_HOSTS debe estar configurada en producción.")

db_url = os.environ.get('DATABASE_URL')
if not db_url:
    db_user = os.environ.get('AUTH_DB_USER')
    db_password = os.environ.get('AUTH_DB_PASSWORD')
    db_name = os.environ.get('AUTH_DB_NAME')
    db_host = os.environ.get('DB_HOST', 'db_central')
    db_port = os.environ.get('DB_PORT', '5432')
    if db_user and db_password and db_name:
        db_url = f'postgres://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

DATABASES = {
    'default': dj_database_url.config(
        default=db_url,
        conn_max_age=600
    )
}
if not DATABASES['default']:
    raise ValueError("CRÍTICO: La base de datos centralizada debe estar configurada mediante DATABASE_URL o variables individuales (AUTH_DB_*) en producción.")

# Configuración REST_AUTH estricta (HttpOnly, Secure y SameSite contra CSRF y XSS)
REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': 'access',
    'JWT_AUTH_REFRESH_COOKIE': 'refresh',
    'JWT_AUTH_HTTPONLY': True,
    'JWT_AUTH_SECURE': True,
    'JWT_AUTH_SAMESITE': 'Lax',
    'JWT_AUTH_RETURN_EXPIRATION': True,
}

from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
}

# CORS estricto en producción
CORS_ALLOWED_ORIGINS = os.environ.get('AUTH_CORS_ALLOWED_ORIGINS', '').split(',')
if not CORS_ALLOWED_ORIGINS or CORS_ALLOWED_ORIGINS == ['']:
    raise ValueError("CRÍTICO: La variable AUTH_CORS_ALLOWED_ORIGINS debe estar configurada para limitar accesos externos.")

# Configuración de email segura en producción
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('AUTH_EMAIL_HOST')
EMAIL_PORT = int(os.environ.get('AUTH_EMAIL_PORT', 587))
EMAIL_HOST_USER = os.environ.get('AUTH_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('AUTH_EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.environ.get('AUTH_EMAIL_USE_TLS', 'True') == 'True'
DEFAULT_FROM_EMAIL = os.environ.get('AUTH_DEFAULT_FROM_EMAIL', 'webmaster@localhost')

# Cabeceras de seguridad HTTP de producción adicionales
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'
SECURE_SSL_REDIRECT = os.environ.get('AUTH_SECURE_SSL_REDIRECT', 'True') == 'True'
