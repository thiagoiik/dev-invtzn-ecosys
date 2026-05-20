from .base import *
import dj_database_url

SECRET_KEY = os.environ.get('INVTZN_DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("La variable INVTZN_DJANGO_SECRET_KEY debe estar configurada en el entorno Sandbox.")

DEBUG = os.environ.get('INVTZN_DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('INVTZN_DJANGO_ALLOWED_HOSTS', '').split(',')

db_url = os.environ.get('DATABASE_URL')
if not db_url:
    db_user = os.environ.get('API_INVTZN_DB_USER', 'api_invtzn_user')
    db_password = os.environ.get('API_INVTZN_DB_PASSWORD', 'invtzn-api-password-secure')
    db_name = os.environ.get('API_INVTZN_DB_NAME', 'api_invtzn_db')
    db_host = os.environ.get('DB_HOST', 'db_central')
    db_port = os.environ.get('DB_PORT', '5432')
    db_url = f'postgres://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

DATABASES = {
    'default': dj_database_url.config(
        default=db_url,
        conn_max_age=600
    )
}

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = os.environ.get('INVTZN_CORS_ALLOWED_ORIGINS', '').split(',')

# Stripe Settings Sandbox (Modo de pruebas real de Stripe)
STRIPE_API_KEY = os.environ.get('STRIPE_API_KEY')
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')
STRIPE_CONNECT_CLIENT_ID = os.environ.get('STRIPE_CONNECT_CLIENT_ID')
