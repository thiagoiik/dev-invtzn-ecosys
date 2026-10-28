import os
from celery import Celery

# Establecer las configuraciones de Django por defecto para Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'invtzn_core.settings.dev')

app = Celery('invtzn_core')

# Usar una cadena aquí significa que el worker no tiene que serializar
# el objeto de configuración a los procesos hijo.
# - namespace='CELERY' significa que todas las llaves de configuración
#   relacionadas con Celery deben tener el prefijo 'CELERY_'.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Cargar las tareas (tasks.py) de todas las aplicaciones Django registradas.
app.autodiscover_tasks()
