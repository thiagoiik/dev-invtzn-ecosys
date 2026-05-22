from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
import logging
from .models import Order
from deployments.models import Deployment
from inventory.models import StoreStock

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Order)
def activate_deployment_on_payment(sender, instance, created, **kwargs):
    """
    Cuando una orden se marca como COMPLETED:
    1. Activamos automáticamente el despliegue asociado (si existe).
    2. Descontamos stock de los productos físicos.
    """
    if instance.status == Order.StatusChoices.COMPLETED:
        # 1. Activación de Deployment
        if instance.deployment:
            deployment = instance.deployment
            if deployment.status != Deployment.StatusChoices.LIVE:
                deployment.status = Deployment.StatusChoices.LIVE
                deployment.is_paid = True
                deployment.save()
                print(f"DEBUG: Deployment {deployment.id} activado por pago de Orden {instance.id}")
        
        # 2. Descuento de Stock
        if not instance.is_stock_deducted:
            with transaction.atomic():
                try:
                    order = Order.objects.select_for_update().get(id=instance.id)
                except Order.DoesNotExist:
                    return
                
                if not order.is_stock_deducted:
                    for item in order.items.all():
                        if item.product.is_physical:
                            # 1. Stock global
                            product = item.product
                            if product.stock_quantity < item.quantity:
                                logger.warning(
                                    f"Alerta de stock: Producto '{product.name}' (ID {product.id}) "
                                    f"tiene stock insuficiente ({product.stock_quantity} disponible, "
                                    f"se requieren {item.quantity}). Procediendo con stock negativo."
                                )
                            product.stock_quantity -= item.quantity
                            product.save()
                            
                            # 2. Stock por sucursal si aplica
                            if order.store:
                                store_stock, _ = StoreStock.objects.get_or_create(
                                    store=order.store,
                                    product=product,
                                    defaults={'quantity': 0}
                                )
                                if store_stock.quantity < item.quantity:
                                    logger.warning(
                                        f"Alerta de stock sucursal '{order.store.name}': "
                                        f"Producto '{product.name}' (ID {product.id}) "
                                        f"tiene stock insuficiente ({store_stock.quantity} disponible, "
                                        f"se requieren {item.quantity}). Procediendo."
                                    )
                                store_stock.quantity -= item.quantity
                                store_stock.save()

                    # Marcar como descontado
                    order.is_stock_deducted = True
                    order.save(update_fields=['is_stock_deducted'])
                    instance.is_stock_deducted = True
