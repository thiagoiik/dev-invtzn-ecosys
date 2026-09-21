from django.db import models
from deployments.models import Deployment

class DeploymentMetric(models.Model):
    class MetricType(models.TextChoices):
        VISIT = 'VISIT', 'Visita'
        RSVP_SUBMIT = 'RSVP_SUBMIT', 'Confirmación de Asistencia'

    deployment = models.ForeignKey(Deployment, on_delete=models.CASCADE, related_name='metrics', db_constraint=False)
    metric_type = models.CharField(max_length=20, choices=MetricType.choices, default=MetricType.VISIT)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True, default='Desconocido')
    country = models.CharField(max_length=100, null=True, blank=True, default='Desconocido')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.metric_type} en {self.deployment.slug} ({self.city}, {self.country})"


class SystemLog(models.Model):
    class LogType(models.TextChoices):
        USER_ACTION = 'USER_ACTION', 'User Action'
        DEPLOYMENT_STATE = 'DEPLOYMENT_STATE', 'Deployment State'
        PAYMENT_FLOW = 'PAYMENT_FLOW', 'Payment Flow'

    log_type = models.CharField(max_length=50, choices=LogType.choices)
    message = models.TextField()
    user_id = models.IntegerField(null=True, blank=True)
    username = models.CharField(max_length=150, null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.log_type} - {self.message[:50]}"


class SessionRecording(models.Model):
    """
    Modelo para almacenar las grabaciones de rrweb (Telemetría UI/UX)
    """
    user_id = models.IntegerField(null=True, blank=True, help_text="ID del usuario que reporta/navega")
    role = models.CharField(max_length=50, null=True, blank=True)
    environment = models.CharField(max_length=50, default='sandbox')
    
    # rrweb payload
    events_payload = models.JSONField(help_text="Payload masivo de eventos DOM de rrweb")
    
    user_agent = models.TextField(null=True, blank=True)
    window_width = models.IntegerField(null=True, blank=True)
    window_height = models.IntegerField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recording from User {self.user_id} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
