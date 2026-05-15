from django.db import models
from decimal import Decimal

class UserProfile(models.Model):
    # Opciones predefinidas (Enums) para asegurar integridad de datos
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'
        VENDOR = 'VENDOR', 'Vendedor'
        DESIGNER = 'DESIGNER', 'Diseñador'
        CLIENT = 'CLIENT', 'Cliente'

    class CustomerType(models.TextChoices):
        LEAD = 'LEAD', 'Prospecto'
        ACTIVE = 'ACTIVE', 'Activo'
        VIP = 'VIP', 'VIP'

    class VendorMode(models.TextChoices):
        PHYSICAL = 'PHYSICAL', 'En Tienda (Físico)'
        REMOTE = 'REMOTE', 'A distancia (Remoto)'

    # PK explícita: Vinculada directamente al ID del token JWT de api-auth
    remote_auth_id = models.IntegerField(primary_key=True)
    
    # Campos de perfil y CRM
    full_name = models.CharField(max_length=255, blank=True, null=True, help_text="Nombre completo sincronizado desde api-auth")
    custom_role = models.CharField(max_length=20, choices=Role.choices, default=Role.CLIENT)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    customer_type = models.CharField(max_length=20, choices=CustomerType.choices, default=CustomerType.LEAD)
    internal_notes = models.TextField(blank=True, null=True, help_text="Notas del CRM para vendedores")
    
    # Configuración de Vendedor
    vendor_mode = models.CharField(max_length=20, choices=VendorMode.choices, default=VendorMode.REMOTE)
    assigned_store = models.ForeignKey('inventory.Store', on_delete=models.SET_NULL, null=True, blank=True, related_name='staff')
    
    # Campos financieros
    base_commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'), help_text="Porcentaje ej. 15.00")
    current_balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), help_text="Saldo a favor del cliente")
    
    # Timestamps automáticos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_authenticated(self):
        """
        Propiedad necesaria para que DRF (Django Rest Framework) pase la validación 
        del permiso IsAuthenticated, ya que este modelo no hereda de AbstractBaseUser.
        """
        return True

    @property
    def id(self):
        """
        Alias para la primary key (remote_auth_id). 
        DRF y las vistas de Django suelen esperar que el usuario tenga un atributo .id
        """
        return self.remote_auth_id

    def __str__(self):
        return f"Perfil {self.remote_auth_id} - {self.get_custom_role_display()}"


class WalletLog(models.Model):
    class Reason(models.TextChoices):
        REFUND = 'REFUND', 'Reembolso'
        BANK_DEPOSIT = 'BANK_DEPOSIT', 'Depósito Bancario'
        PURCHASE = 'PURCHASE', 'Compra / Cargo'

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='wallet_logs')
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Valores positivos (ingresos) o negativos (cargos)")
    reason = models.CharField(max_length=20, choices=Reason.choices)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User {self.user_id} | {self.amount} | {self.get_reason_display()}"


class CommunicationLog(models.Model):
    class Channel(models.TextChoices):
        EMAIL = 'EMAIL', 'Correo Electrónico'
        WHATSAPP = 'WHATSAPP', 'WhatsApp'
        VOIP = 'VOIP', 'Llamada VoIP'
        SYSTEM = 'SYSTEM', 'Notificación de Sistema'

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='communications')
    channel = models.CharField(max_length=20, choices=Channel.choices)
    subject = models.CharField(max_length=255)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.channel} a User {self.user_id}: {self.subject}"