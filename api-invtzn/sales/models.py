from django.db import models
from django.contrib.auth import get_user_model
from inventory.models import Product
from deployments.models import Deployment

User = get_user_model()

class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'PENDING', 'Pendiente'
        COMPLETED = 'COMPLETED', 'Completado'
        REFUNDED = 'REFUNDED', 'Reembolsado'

    class OriginChoices(models.TextChoices):
        ONLINE = 'ONLINE', 'Tienda Online / B2C'
        POS = 'POS', 'Punto de Venta / B2B'

    class FulfillmentStatusChoices(models.TextChoices):
        PENDING = 'PENDING', 'Pendiente'
        IN_PRODUCTION = 'IN_PRODUCTION', 'En Producción'
        SHIPPED = 'SHIPPED', 'Enviado'
        DELIVERED = 'DELIVERED', 'Entregado'

    user = models.IntegerField(db_index=True, help_text="ID del usuario en api-auth")
    vendor_id = models.IntegerField(null=True, blank=True, help_text="ID del vendedor que registró la orden")
    deployment = models.ForeignKey(Deployment, on_delete=models.SET_NULL, null=True, blank=True)
    
    subtotal_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    coupon = models.ForeignKey('sales.Coupon', on_delete=models.SET_NULL, null=True, blank=True)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    origin = models.CharField(max_length=20, choices=OriginChoices.choices, default=OriginChoices.ONLINE)
    store = models.ForeignKey('inventory.Store', on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    customer_email = models.EmailField(blank=True, null=True, help_text="Correo electrónico para enviar el recibo")
    fulfillment_status = models.CharField(
        max_length=20, 
        choices=FulfillmentStatusChoices.choices, 
        default=FulfillmentStatusChoices.PENDING
    )
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    is_stock_deducted = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Orden #{self.id} - User {self.user} ({self.status})"

    @property
    def product(self):
        first_item = self.items.first()
        return first_item.product if first_item else None


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price_at_sale = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio cobrado al momento de la compra")

    def __str__(self):
        return f"Item: {self.product.name} x {self.quantity} en Orden #{self.order.id}"

class PaymentTransaction(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    provider = models.CharField(max_length=50, default='Stripe')
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    
    # Stripe specific tracking
    stripe_checkout_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    stripe_payment_intent_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    
    payment_method = models.CharField(max_length=50, default='CARD', help_text="CARD, BANK_TRANSFER, CASH")
    success = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pago de Orden #{self.order.id} - Exitoso: {self.success}"

class CashSession(models.Model):
    user = models.IntegerField(help_text="ID del vendedor que abre caja")
    store = models.ForeignKey('inventory.Store', on_delete=models.CASCADE, related_name='cash_sessions')
    
    opening_balance = models.DecimalField(max_digits=10, decimal_places=2)
    closing_balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    is_open = models.BooleanField(default=True)
    opened_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Turno {self.id} - {self.store.name} (Abierto: {self.is_open})"

class Commission(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='commission')
    vendor_id = models.IntegerField(help_text="ID del vendedor comisionista")
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comisión de ${self.amount} para Vendedor {self.vendor_id}"

class Invoice(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='invoice')
    rfc = models.CharField(max_length=13)
    razon_social = models.CharField(max_length=255)
    codigo_postal = models.CharField(max_length=5)
    regimen_fiscal = models.CharField(max_length=3)
    uso_cfdi = models.CharField(max_length=3)
    uuid = models.CharField(max_length=36, unique=True, help_text="Folio Fiscal SAT (UUID)")
    pdf_url = models.URLField(max_length=500, blank=True, null=True)
    xml_url = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CFDI {self.uuid} - Orden #{self.order.id} ({self.rfc})"

class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='shipping_address')
    recipient_name = models.CharField(max_length=200)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"Dirección de envío para Orden #{self.order.id} - {self.recipient_name}"

class Coupon(models.Model):
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
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='direct_discount')
    authorized_by = models.IntegerField(help_text="ID del Franquiciatario/Admin que autorizó")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField(help_text="Justificación del descuento (Cortesía, Cliente VIP, etc.)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Descuento de {self.amount} autorizado por {self.authorized_by}"
