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

    user = models.IntegerField(db_index=True, help_text="ID del usuario en api-auth")
    vendor_id = models.IntegerField(null=True, blank=True, help_text="ID del vendedor que registró la orden")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True, blank=True)
    deployment = models.ForeignKey(Deployment, on_delete=models.SET_NULL, null=True, blank=True)
    
    subtotal_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    origin = models.CharField(max_length=20, choices=OriginChoices.choices, default=OriginChoices.ONLINE)
    store = models.ForeignKey('inventory.Store', on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Orden #{self.id} - User {self.user} ({self.status})"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price_at_sale = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} en Orden #{self.order.id}"


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
