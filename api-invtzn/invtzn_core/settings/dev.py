from .base import *
import dj_database_url

SECRET_KEY = os.environ.get('INVTZN_DJANGO_SECRET_KEY', 'django-insecure-api-invtzn-8n9vs72itf!k%^-mzv!iuqv@!bl-^52^8')

DEBUG = os.environ.get('INVTZN_DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('INVTZN_DJANGO_ALLOWED_HOSTS', 'api.invtzn.local,localhost,127.0.0.1').split(',')

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

# Si estamos ejecutando tests, forzamos SQLite
if 'test' in sys.argv or 'pytest' in sys.modules:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test_db.sqlite3',
    }

# CORS de desarrollo
CORS_ALLOW_ALL_ORIGINS = True  # Solo para desarrollo local
CORS_ALLOWED_ORIGINS = os.environ.get(
    'INVTZN_CORS_ALLOWED_ORIGINS', 
    'http://front.auth.local,http://localhost:5173'
).split(',')

# Stripe Settings
STRIPE_API_KEY = os.environ.get('STRIPE_API_KEY', 'sk_test_placeholder')
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET', 'whsec_placeholder')
STRIPE_CONNECT_CLIENT_ID = os.environ.get('STRIPE_CONNECT_CLIENT_ID', 'ca_placeholder')
