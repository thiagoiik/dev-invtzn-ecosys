from .base import *
import dj_database_url

# Sandbox requiere obligatoriamente que las variables de entorno estén bien seteadas
SECRET_KEY = os.environ.get('AUTH_DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("La variable AUTH_DJANGO_SECRET_KEY debe estar configurada en el entorno Sandbox.")

DEBUG = os.environ.get('AUTH_DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('AUTH_DJANGO_ALLOWED_HOSTS', '').split(',')

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
    raise ValueError("CRÍTICO: La base de datos centralizada debe estar configurada en el entorno Sandbox.")

# Configuración REST_AUTH (HTTPS recomendado en Sandbox pero HTTP disponible si es necesario)
REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': 'access',
    'JWT_AUTH_REFRESH_COOKIE': 'refresh',
    'JWT_AUTH_HTTPONLY': True,
    'JWT_AUTH_SECURE': os.environ.get('AUTH_JWT_SECURE', 'False') == 'True',
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

CORS_ALLOWED_ORIGINS = os.environ.get('AUTH_CORS_ALLOWED_ORIGINS', '').split(',')

# Configuración de email en Sandbox
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('AUTH_EMAIL_HOST')
EMAIL_PORT = int(os.environ.get('AUTH_EMAIL_PORT', 587))
EMAIL_HOST_USER = os.environ.get('AUTH_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('AUTH_EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.environ.get('AUTH_EMAIL_USE_TLS', 'True') == 'True'
DEFAULT_FROM_EMAIL = os.environ.get('AUTH_DEFAULT_FROM_EMAIL', 'webmaster@localhost')
