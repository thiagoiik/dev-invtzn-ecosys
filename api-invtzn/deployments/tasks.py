import os
import logging
import requests
from celery import shared_task
from .models import Deployment, DeploymentMetric

logger = logging.getLogger(__name__)

@shared_task(name='deployments.tasks.record_metric_task')
def record_metric_task(deployment_id, metric_type, ip_address, user_agent):
    try:
        deployment = Deployment.objects.get(id=deployment_id)
    except Deployment.DoesNotExist:
        logger.error(f"Deployment con ID {deployment_id} no existe.")
        return False

    city = 'Desconocido'
    country = 'Desconocido'

    # Enrutar IPs locales/privadas sin realizar llamadas externas
    # Incluye localhost, redes privadas clase A (10.*), clase C (192.168.*) y clase B de Docker (172.16.0.0/12)
    is_local = False
    if ip_address in ['127.0.0.1', 'localhost', '::1', None]:
        is_local = True
    elif ip_address.startswith('192.168.') or ip_address.startswith('10.'):
        is_local = True
    elif ip_address.startswith('172.'):
        parts = ip_address.split('.')
        if len(parts) >= 2:
            try:
                second_octet = int(parts[1])
                if 16 <= second_octet <= 31:
                    is_local = True
            except ValueError:
                pass

    if is_local:
        city = 'Localhost'
        country = 'México'
    else:
        geoip_db_path = os.environ.get('GEOIP_DATABASE_PATH')
        resolved = False

        # Intentar geolocalización local mediante base de datos MaxMind en producción
        if geoip_db_path and os.path.exists(geoip_db_path):
            try:
                import geoip2.database
                with geoip2.database.Reader(geoip_db_path) as reader:
                    response = reader.city(ip_address)
                    country = response.country.names.get('es') or response.country.name or 'Desconocido'
                    city = response.city.names.get('es') or response.city.name or 'Desconocido'
                    resolved = True
            except Exception as e:
                logger.warning(f"Error resolviendo IP {ip_address} localmente con MaxMind: {e}. Se usará fallback de API.")

        # Fallback a API pública externa si no se pudo resolver localmente o no está configurada la BD
        if not resolved:
            try:
                # Petición a ip-api con un timeout de 2.0s
                geo_res = requests.get(f"http://ip-api.com/json/{ip_address}", timeout=2.0).json()
                if geo_res.get('status') == 'success':
                    city = geo_res.get('city', 'Desconocido')
                    country = geo_res.get('country', 'Desconocido')
            except Exception as e:
                logger.warning(f"Error resolviendo geolocalización para IP {ip_address} con ip-api: {e}")

    try:
        DeploymentMetric.objects.create(
            deployment=deployment,
            metric_type=metric_type,
            ip_address=ip_address,
            user_agent=user_agent[:500] if user_agent else '',
            city=city,
            country=country
        )
        return True
    except Exception as e:
        logger.error(f"Error al crear DeploymentMetric: {e}")
        return False

