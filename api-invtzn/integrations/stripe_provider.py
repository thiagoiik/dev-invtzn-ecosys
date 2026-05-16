import stripe
from django.conf import settings
from django.urls import reverse

class StripeProvider:
    @staticmethod
    def _set_api_key():
        import stripe
        from django.conf import settings
        stripe.api_key = getattr(settings, 'STRIPE_API_KEY', None)

    @staticmethod
    def create_onboarding_link(store, return_url, refresh_url):
        StripeProvider._set_api_key()
        import stripe
        """
        Crea un enlace de onboarding para una cuenta de Stripe Connect.
        Si la tienda no tiene stripe_account_id, se crea una nueva cuenta Express.
        """
        if not store.stripe_account_id:
            account = stripe.Account.create(
                type="express",
                country="MX", # Ajustar según sea necesario
                email=getattr(store, 'email', None), # Asumiendo que Store tiene email o similar
                capabilities={
                    "card_payments": {"requested": True},
                    "transfers": {"requested": True},
                },
            )
            store.stripe_account_id = account.id
            store.save()

        account_link = stripe.AccountLink.create(
            account=store.stripe_account_id,
            refresh_url=refresh_url,
            return_url=return_url,
            type="account_onboarding",
        )
        return account_link.url

    @staticmethod
    def create_checkout_session(order, success_url, cancel_url):
        StripeProvider._set_api_key()
        import stripe
        """
        Crea una sesión de Checkout para una orden.
        Si la orden pertenece a una tienda con Connect, se configura la transferencia.
        """
        store = order.store
        checkout_params = {
            "payment_method_types": ["card"],
            "line_items": [{
                "price_data": {
                    "currency": "mxn",
                    "product_data": {
                        "name": f"Orden #{order.id} - {order.product.name}",
                    },
                    "unit_amount": int(order.total_amount * 100),
                },
                "quantity": 1,
            }],
            "mode": "payment",
            "success_url": success_url,
            "cancel_url": cancel_url,
            "metadata": {
                "order_id": order.id,
            },
        }

        # Si la tienda tiene Connect configurado, enviamos el pago a su cuenta
        if store and store.stripe_account_id and store.stripe_onboarding_completed:
            checkout_params["payment_intent_data"] = {
                "transfer_data": {
                    "destination": store.stripe_account_id,
                },
            }

        session = stripe.checkout.Session.create(**checkout_params)
        
        # Guardar el ID de la sesión en la transacción
        from sales.models import PaymentTransaction
        PaymentTransaction.objects.update_or_create(
            order=order,
            defaults={
                'stripe_checkout_id': session.id,
                'provider': 'Stripe'
            }
        )
        
        return session.url

    @staticmethod
    def handle_webhook(payload, sig_header):
        StripeProvider._set_api_key()
        import stripe
        """
        Maneja los eventos de Stripe Webhook.
        """
        event = None
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError:
            return False, "Invalid payload"
        except stripe.error.SignatureVerificationError:
            return False, "Invalid signature"

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            order_id = session.get('metadata', {}).get('order_id')
            if order_id:
                StripeProvider._complete_order(order_id, session)

        return True, "Success"

    @staticmethod
    def _complete_order(order_id, session):
        from sales.models import Order, PaymentTransaction
        from deployments.models import Deployment
        try:
            order = Order.objects.get(id=order_id)
            order.status = Order.StatusChoices.COMPLETED
            order.save()

            # Activar el Deployment si existe
            if order.deployment:
                order.deployment.is_paid = True
                order.deployment.status = Deployment.StatusChoices.LIVE
                order.deployment.save()

            transaction = order.payment
            transaction.success = True
            transaction.stripe_payment_intent_id = session.get('payment_intent')
            transaction.save()
        except Order.DoesNotExist:
            pass

    @staticmethod
    def check_onboarding_status(store):
        StripeProvider._set_api_key()
        import stripe
        """
        Consulta a Stripe si el onboarding de la cuenta Connect se ha completado.
        """
        if not store.stripe_account_id:
            return False
            
        try:
            account = stripe.Account.retrieve(store.stripe_account_id)
            if account.details_submitted:
                store.stripe_onboarding_completed = True
                store.save()
                return True
        except Exception as e:
            print(f"Error verificando onboarding: {e}")
            
        return False
