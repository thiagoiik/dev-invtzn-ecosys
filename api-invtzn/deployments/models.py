from django.db import models
from django.contrib.auth import get_user_model
from inventory.models import Product

User = get_user_model()

class Deployment(models.Model):
    class StatusChoices(models.TextChoices):
        DRAFT = 'DRAFT', 'Borrador / Sandbox'
        LIVE = 'LIVE', 'Publicado'
        EXPIRED = 'EXPIRED', 'Expirado / Inactivo'

    user = models.IntegerField(db_index=True, help_text="ID del usuario en api-auth")
    vendor_id = models.IntegerField(null=True, blank=True, help_text="ID del vendedor que registró el diseño")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='deployments')
    
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True, help_text="URL única para acceso público")
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.DRAFT)
    
    custom_data = models.JSONField(default=dict, blank=True, help_text="Almacena el diseño de Pinia")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            import uuid
            self.slug = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.slug or 'Draft'} - User {self.user} ({self.status})"

class Guest(models.Model):
    deployment = models.ForeignKey(Deployment, on_delete=models.CASCADE, related_name='guests')
    full_name = models.CharField(max_length=150)
    attending = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {'Asiste' if self.attending else 'No asiste'} ({self.deployment.slug})"
