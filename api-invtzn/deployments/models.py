from django.db import models
from django.contrib.auth import get_user_model
from inventory.models import Product

User = get_user_model()

class Deployment(models.Model):
    class StatusChoices(models.TextChoices):
        DRAFT = 'DRAFT', 'Borrador / Sandbox'
        LIVE = 'LIVE', 'Publicado'
        EXPIRED = 'EXPIRED', 'Expirado / Inactivo'

    class CreationMode(models.TextChoices):
        CATALOG = 'CATALOG', 'Catalog'
        CANVAS = 'CANVAS', 'Canvas'

    user = models.IntegerField(db_index=True, null=True, blank=True, help_text="ID del usuario en api-auth")
    vendor_id = models.IntegerField(null=True, blank=True, help_text="ID del vendedor que registró el diseño")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='deployments')
    
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True, help_text="URL única para acceso público")
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.DRAFT)
    is_paid = models.BooleanField(default=False, help_text="Indica si la invitación ya fue pagada")
    creation_mode = models.CharField(max_length=20, choices=CreationMode.choices, default=CreationMode.CANVAS, help_text="Modo de creación")
    
    custom_data = models.JSONField(default=dict, blank=True, help_text="Almacena el diseño de Pinia")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            if self.product and getattr(self.product, 'template_slug', None):
                try:
                    from deployments.models import Deployment as DepModel
                    template_dep = DepModel.objects.get(slug=self.product.template_slug)
                    if not self.custom_data or self.custom_data == {}:
                        import copy
                        self.custom_data = copy.deepcopy(template_dep.custom_data)
                        self.creation_mode = template_dep.creation_mode
                except Exception:
                    pass

        if not self.slug:
            import uuid
            self.slug = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.slug or 'Draft'} - User {self.user} ({self.status})"

    @property
    def allowed_features(self):
        # Características mínimas por defecto (Básica)
        features = {
            'background_music': False,
            'custom_audio_url': False,
            'countdown_timer': False,
            'timeline': False,
            'custom_theme': False,
            'custom_og': False,
        }

        if not self.product:
            return features

        tier = self.product.tier_level
        
        # Mapeo de características heredadas por Tier comercial
        if tier == 'PREMIUM':
            features.update({
                'background_music': True,
                'custom_audio_url': True,
                'countdown_timer': True,
                'timeline': True,
                'custom_theme': True,
                'custom_og': True,
            })
        elif tier == 'STANDARD':
            features.update({
                'background_music': True,
                'custom_audio_url': False,
                'countdown_timer': True,
                'timeline': False,
                'custom_theme': True,
                'custom_og': False,
            })
        elif tier == 'BASIC':
            features.update({
                'background_music': False,
                'custom_audio_url': False,
                'countdown_timer': False,
                'timeline': False,
                'custom_theme': True,
                'custom_og': False,
            })

        # Si el JSON 'features' de Product contiene sobrescrituras específicas, las aplicamos
        if isinstance(self.product.features, dict):
            features.update(self.product.features)

        return features

class Event(models.Model):
    title = models.CharField(max_length=200, help_text="Ej: Boda de Ana y Jorge")
    owner = models.IntegerField(db_index=True, help_text="ID del usuario en api-auth")
    event_date = models.DateTimeField(null=True, blank=True)
    location_name = models.CharField(max_length=200, blank=True)
    
    deployments = models.ManyToManyField(Deployment, blank=True, related_name='linked_events')
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.event_date.strftime('%Y-%m-%d') if self.event_date else 'Sin fecha'}"

class Guest(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'PENDING', 'Pendiente de Aprobación'
        APPROVED = 'APPROVED', 'Aprobado (QR Emitido)'
        DENIED = 'DENIED', 'Denegado'

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='guests', null=True, blank=True)
    deployment = models.ForeignKey(Deployment, on_delete=models.CASCADE, related_name='guests', null=True, blank=True)
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20, blank=True, null=True, help_text="Para enviar el QR por WhatsApp")
    email = models.EmailField(blank=True, null=True)
    
    attending = models.BooleanField(default=True)
    companions_count = models.IntegerField(default=0, help_text="Número de acompañantes extra")
    
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    
    qr_code_token = models.CharField(max_length=64, unique=True, blank=True, null=True, help_text="Token seguro para generar el QR")
    qr_scanned = models.BooleanField(default=False, help_text="¿Ya ingresó al salón?")
    scanned_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.status == self.StatusChoices.APPROVED and not self.qr_code_token:
            import secrets
            self.qr_code_token = secrets.token_hex(16)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.status})"

class DeploymentMetric(models.Model):
    class MetricType(models.TextChoices):
        VISIT = 'VISIT', 'Visita'
        RSVP_SUBMIT = 'RSVP_SUBMIT', 'Confirmación de Asistencia'

    deployment = models.ForeignKey(Deployment, on_delete=models.CASCADE, related_name='metrics')
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
