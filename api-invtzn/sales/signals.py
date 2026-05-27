from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
import logging
from .models import Order
from deployments.models import Deployment, SystemLog
from inventory.models import StoreStock

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Order)
def activate_deployment_on_payment(sender, instance, created, **kwargs):
    """
    Cuando una orden se marca como COMPLETED:
    1. Activamos automáticamente el despliegue asociado (si existe), cambiamos su producto al de la orden.
    2. Descontamos stock de los productos físicos.
    3. Registramos eventos en SystemLog.
    """
    if instance.status == Order.StatusChoices.COMPLETED and not instance.is_stock_deducted:
        # Buscar username si es posible
        username = None
        if instance.user:
            from profiles.models import UserProfile
            try:
                profile = UserProfile.objects.get(remote_auth_id=instance.user)
                username = profile.email or profile.full_name or f"user_{instance.user}"
            except UserProfile.DoesNotExist:
                pass

        # 1. Activación de Deployment y cambio de producto
        if instance.deployment:
            deployment = instance.deployment
            order_product = instance.product
            modified = False
            if order_product and deployment.product != order_product:
                deployment.product = order_product
                modified = True
            if deployment.status != Deployment.StatusChoices.LIVE:
                deployment.status = Deployment.StatusChoices.LIVE
                modified = True
            if not deployment.is_paid:
                deployment.is_paid = True
                modified = True
            if modified:
                deployment.save()
                print(f"DEBUG: Deployment {deployment.id} activado y actualizado por pago de Orden {instance.id}")

            # Registrar log del cambio de estado del Deployment
            SystemLog.objects.create(
                log_type=SystemLog.LogType.DEPLOYMENT_STATE,
                message=f"Deployment {deployment.slug} (ID: {deployment.id}) product updated to {deployment.product.name if deployment.product else 'None'} and activated (LIVE, paid).",
                user_id=instance.user,
                username=username,
                metadata={
                    'deployment_id': deployment.id,
                    'slug': deployment.slug,
                    'product_id': deployment.product.id if deployment.product else None,
                    'order_id': instance.id,
                    'is_paid': deployment.is_paid,
                    'status': deployment.status
                }
            )

        # Registrar log de flujo de pago (Stripe o POS/General)
        is_stripe = False
        payment_method = "UNKNOWN"
        provider = "UNKNOWN"
        try:
            if hasattr(instance, 'payment') and instance.payment:
                is_stripe = (instance.payment.provider == 'Stripe')
                payment_method = instance.payment.payment_method
                provider = instance.payment.provider
        except Exception:
            pass

        log_msg = f"Payment flow completed for Order #{instance.id}."
        if is_stripe:
            log_msg = f"Stripe payment webhook completed for Order #{instance.id}."

        SystemLog.objects.create(
            log_type=SystemLog.LogType.PAYMENT_FLOW,
            message=log_msg,
            user_id=instance.user,
            username=username,
            metadata={
                'order_id': instance.id,
                'total_amount': str(instance.total_amount),
                'payment_provider': provider,
                'payment_method': payment_method,
                'is_stripe': is_stripe
            }
        )
        
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
