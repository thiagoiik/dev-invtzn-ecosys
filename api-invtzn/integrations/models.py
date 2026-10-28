from django.db import models

class BankSyncLog(models.Model):
    external_id = models.CharField(max_length=255, unique=True, help_text="ID de la transacción en el banco (STP/BBVA)")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    sender_name = models.CharField(max_length=255, blank=True, null=True)
    sender_bank = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    is_reconciled = models.BooleanField(default=False)
    reconciled_at = models.DateTimeField(null=True, blank=True)
    order = models.OneToOneField('sales.Order', on_delete=models.SET_NULL, null=True, blank=True, related_name='bank_sync')

    timestamp = models.DateTimeField(help_text="Fecha y hora del movimiento bancario")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Movimiento {self.external_id} - ${self.amount}"

class WebhookLog(models.Model):
    provider = models.CharField(max_length=50, default='Stripe')
    payload = models.JSONField(blank=True, null=True, help_text="Cuerpo de la petición recibida")
    headers = models.JSONField(blank=True, null=True, help_text="Cabeceras HTTP recibidas")
    status = models.CharField(max_length=50, help_text="success, failed, ignored")
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Webhook {self.provider} - {self.status} ({self.created_at})"
