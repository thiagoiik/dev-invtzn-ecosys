from django.db import models
from django.contrib.auth import get_user_model
from inventory.models import Product
from .models import Deployment

User = get_user_model()

# ==========================================
# 1. MÓDULO DE EVENTOS Y RSVP AVANZADO
# ==========================================

class Event(models.Model):
    """
    Desacopla la celebración física (fecha, lugar, dueños) de la invitación visual (Deployment).
    Un evento puede tener 1 o más Deployments (ej. Save the date, Invitación Formal, Agradecimiento).
    """
    title = models.CharField(max_length=200, help_text="Ej: Boda de Ana y Jorge")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    event_date = models.DateTimeField(null=True, blank=True)
    location_name = models.CharField(max_length=200, blank=True)
    
    # Vinculación opcional a múltiples diseños
    deployments = models.ManyToManyField(Deployment, blank=True, related_name='linked_events')
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.event_date.strftime('%Y-%m-%d') if self.event_date else 'Sin fecha'}"

class Guest(models.Model):
    """
    Reemplaza al Guest actual. Ahora está atado al Evento, no al diseño.
    Añadimos control de acceso y flujos de aprobación.
    """
    class StatusChoices(models.TextChoices):
        PENDING = 'PENDING', 'Pendiente de Aprobación'
        APPROVED = 'APPROVED', 'Aprobado (QR Emitido)'
        DENIED = 'DENIED', 'Denegado'

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='guests')
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
        # Generar token QR automáticamente al ser aprobado
        if self.status == self.StatusChoices.APPROVED and not self.qr_code_token:
            import secrets
            self.qr_code_token = secrets.token_hex(16)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.status})"

# ==========================================
# 2. MÓDULO DE PROMOCIONES Y CUPONES
# ==========================================

class Coupon(models.Model):
    """
    Cupones públicos que los usuarios ingresan en el Checkout.
    """
    code = models.CharField(max_length=50, unique=True, help_text="Ej: BLACKFRIDAY2026")
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Ej: 15.00 para 15%")
    discount_fixed = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Ej: 500.00 para descontar 500 MXN")
    
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)
    
    max_uses = models.IntegerField(default=100, help_text="Límite de usos totales")
    current_uses = models.IntegerField(default=0)

    def is_valid(self):
        from django.utils import timezone
        now = timezone.now()
        return self.active and self.valid_from <= now <= self.valid_to and self.current_uses < self.max_uses

    def __str__(self):
        return self.code

class DirectDiscount(models.Model):
    """
    Registro auditable de descuentos aplicados manualmente por un administrador o franquiciatario en el POS.
    """
    order = models.OneToOneField('sales.Order', on_delete=models.CASCADE, related_name='direct_discount')
    authorized_by = models.ForeignKey(User, on_delete=models.PROTECT, help_text="Franquiciatario/Admin que autorizó")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField(help_text="Justificación del descuento (Cortesía, Cliente VIP, etc.)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Descuento de {self.amount} autorizado por {self.authorized_by}"
