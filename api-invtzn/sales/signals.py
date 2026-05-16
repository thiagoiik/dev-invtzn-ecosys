from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from deployments.models import Deployment

@receiver(post_save, sender=Order)
def activate_deployment_on_payment(sender, instance, created, **kwargs):
    """
    Cuando una orden se marca como COMPLETED, activamos automáticamente
    el despliegue asociado (si existe).
    """
    if instance.status == Order.StatusChoices.COMPLETED and instance.deployment:
        deployment = instance.deployment
        
        # Solo actualizamos si no está ya en vivo
        if deployment.status != Deployment.StatusChoices.LIVE:
            deployment.status = Deployment.StatusChoices.LIVE
            deployment.is_paid = True
            deployment.save()
            print(f"DEBUG: Deployment {deployment.id} activado por pago de Orden {instance.id}")
