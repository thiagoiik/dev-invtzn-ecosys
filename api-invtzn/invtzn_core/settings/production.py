from .base import *
import dj_database_url

SECRET_KEY = os.environ.get('INVTZN_DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("CRÍTICO: La variable INVTZN_DJANGO_SECRET_KEY debe estar configurada en producción.")

DEBUG = False

ALLOWED_HOSTS = os.environ.get('INVTZN_DJANGO_ALLOWED_HOSTS', '').split(',')
if not ALLOWED_HOSTS or ALLOWED_HOSTS == ['']:
    raise ValueError("CRÍTICO: La variable INVTZN_DJANGO_ALLOWED_HOSTS debe estar configurada en producción.")

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
    raise ValueError("CRÍTICO: La base de datos centralizada debe estar configurada mediante DATABASE_URL o variables individuales (API_INVTZN_DB_*) en producción.")

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = os.environ.get('INVTZN_CORS_ALLOWED_ORIGINS', '').split(',')
if not CORS_ALLOWED_ORIGINS or CORS_ALLOWED_ORIGINS == ['']:
    raise ValueError("CRÍTICO: La variable INVTZN_CORS_ALLOWED_ORIGINS debe estar configurada para limitar accesos en producción.")

# Stripe Settings Producción (Claves vivas de Stripe)
STRIPE_API_KEY = os.environ.get('STRIPE_API_KEY')
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')
STRIPE_CONNECT_CLIENT_ID = os.environ.get('STRIPE_CONNECT_CLIENT_ID')

if not STRIPE_API_KEY or STRIPE_API_KEY.startswith('sk_test'):
    # Advertencia o error estricto según tu preferencia, aquí lo hacemos estricto
    raise ValueError("CRÍTICO: Intentando usar clave Stripe de Test o nula en entorno de producción real.")

# Cabeceras de seguridad HTTP de producción adicionales
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'
SECURE_SSL_REDIRECT = os.environ.get('INVTZN_SECURE_SSL_REDIRECT', 'True') == 'True'
