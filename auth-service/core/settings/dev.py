from .base import *
import dj_database_url

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('AUTH_DJANGO_SECRET_KEY', 'django-insecure-8n9vs72itf!k%^-mzv!iuqv@!bl-^52^8!nc+@o4*wufpkqvhe')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('AUTH_DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('AUTH_DJANGO_ALLOWED_HOSTS', 'api.auth.local,localhost,127.0.0.1').split(',')

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
db_url = os.environ.get('DATABASE_URL')
if not db_url:
    db_user = os.environ.get('AUTH_DB_USER', 'auth_service_user')
    db_password = os.environ.get('AUTH_DB_PASSWORD', 'auth_password_secure')
    db_name = os.environ.get('AUTH_DB_NAME', 'auth_db_service')
    db_host = os.environ.get('DB_HOST', 'db_central')
    db_port = os.environ.get('DB_PORT', '5432')
    db_url = f'postgres://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

DATABASES = {
    'default': dj_database_url.config(
        default=db_url,
        conn_max_age=600
    )
}

# Configuración REST_AUTH para Desarrollo (Cookies inseguras para localhost)
REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': 'access',
    'JWT_AUTH_REFRESH_COOKIE': 'refresh',
    'JWT_AUTH_HTTPONLY': False,
    'JWT_AUTH_SECURE': False,
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

# CORS locales de desarrollo
CORS_ALLOWED_ORIGINS = os.environ.get(
    'AUTH_CORS_ALLOWED_ORIGINS', 
    'http://front.auth.local,http://localhost:5173'
).split(',')

# Envío de correo en consola para desarrollo
EMAIL_BACKEND = os.environ.get('AUTH_EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
