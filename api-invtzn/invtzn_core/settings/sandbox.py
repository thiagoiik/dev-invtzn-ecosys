from .base import *
import dj_database_url

SECRET_KEY = os.environ.get('INVTZN_DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("La variable INVTZN_DJANGO_SECRET_KEY debe estar configurada en el entorno Sandbox.")

DEBUG = os.environ.get('INVTZN_DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('INVTZN_DJANGO_ALLOWED_HOSTS', '').split(',')

# Configuración de seguridad para Proxy SSL y CSRF
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_TRUSTED_ORIGINS = [f"https://{host.strip()}" for host in ALLOWED_HOSTS if host.strip()]

db_url = os.environ.get('DATABASE_URL')
if not db_url:
    db_user = os.environ.get('API_INVTZN_DB_USER')
    db_password = os.environ.get('API_INVTZN_DB_PASSWORD')
    db_name = os.environ.get('API_INVTZN_DB_NAME')
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

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = os.environ.get('INVTZN_CORS_ALLOWED_ORIGINS', '').split(',')

# Stripe Settings Sandbox (Modo de pruebas real de Stripe)
STRIPE_API_KEY = os.environ.get('STRIPE_API_KEY')
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')
STRIPE_CONNECT_CLIENT_ID = os.environ.get('STRIPE_CONNECT_CLIENT_ID')
