import pytest
from unittest.mock import patch, MagicMock
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APIClient
from integrations.models import BankSyncLog
from integrations.stripe_provider import StripeProvider
from profiles.models import UserProfile
from sales.models import Order, PaymentTransaction
from deployments.models import Deployment
from inventory.models import Product

User = get_user_model()

@pytest.mark.django_db
class TestIntegrations:
    def setup_method(self):
        self.client = APIClient()

        # 1. Crear usuarios y perfiles
        self.admin_user = User.objects.create_user(username='admin_fin', password='password123')
        self.admin_profile = UserProfile.objects.create(remote_auth_id=self.admin_user.id, custom_role=UserProfile.Role.ADMIN)

        self.franchisee_user = User.objects.create_user(username='fran_fin', password='password123')
        self.franchisee_profile = UserProfile.objects.create(remote_auth_id=self.franchisee_user.id, custom_role=UserProfile.Role.FRANCHISEE)

        self.client_user = User.objects.create_user(username='client_fin', password='password123')
        self.client_profile = UserProfile.objects.create(remote_auth_id=self.client_user.id, custom_role=UserProfile.Role.CLIENT)

        # 2. Crear datos base (Productos y Órdenes)
        self.product = Product.objects.create(name="Invitacion Premium", base_price=200.00, product_type=Product.ProductType.DIGITAL)
        self.deployment = Deployment.objects.create(user=self.client_user.id, product=self.product, status=Deployment.StatusChoices.DRAFT, is_paid=False)
        self.order = Order.objects.create(
            user=self.client_user.id,
            deployment=self.deployment,
            total_amount=200.00,
            status=Order.StatusChoices.PENDING
        )
        from sales.models import OrderItem
        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            price_at_sale=200.00
        )

        # 3. Crear registros bancarios
        self.bank_log = BankSyncLog.objects.create(
            external_id="STP-12345",
            amount=200.00,
            sender_name="JUAN PEREZ",
            sender_bank="BBVA",
            description="Pago invitacion",
            timestamp=timezone.now()
        )

    def test_bank_sync_log_representation(self):
        """Verifica el __str__ del log de sincronización bancaria."""
        assert "STP-12345" in str(self.bank_log)
        assert "200" in str(self.bank_log)

    def test_reconciliation_access_admin_allowed(self):
        """Un usuario administrador debe poder ver los movimientos de reconciliación."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/v1/integrations/')
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_reconciliation_access_client_denied(self):
        """Un cliente común no debe tener acceso a ver registros de reconciliación."""
        self.client.force_authenticate(user=self.client_user)
        response = self.client.get('/api/v1/integrations/')
        assert response.status_code == 200
        assert len(response.data) == 0

    def test_sync_order_success(self):
        """Conciliación exitosa: la orden se completa, el log se marca como reconciliado y se genera la transacción."""
        self.client.force_authenticate(user=self.admin_user)
        payload = {
            "bank_log_id": self.bank_log.id,
            "order_id": self.order.id
        }
        response = self.client.post('/api/v1/integrations/sync/', payload)
        assert response.status_code == 200
        
        # Validar cambios en base de datos
        self.order.refresh_from_db()
        self.bank_log.refresh_from_db()
        
        assert self.order.status == Order.StatusChoices.COMPLETED
        assert self.bank_log.is_reconciled is True
        assert self.bank_log.order == self.order
        
        # Validar transacción
        transaction = PaymentTransaction.objects.get(order=self.order)
        assert transaction.provider == 'BANK_SYNC'
        assert transaction.success is True

    def test_sync_order_insufficient_amount(self):
        """Error de conciliación: el monto en el banco es menor al total de la orden."""
        self.bank_log.amount = 150.00
        self.bank_log.save()
        
        self.client.force_authenticate(user=self.admin_user)
        payload = {
            "bank_log_id": self.bank_log.id,
            "order_id": self.order.id
        }
        response = self.client.post('/api/v1/integrations/sync/', payload)
        assert response.status_code == 400
        assert "monto del banco es menor" in response.data['error']

    def test_sync_order_missing_params(self):
        """Error de conciliación: faltan parámetros requeridos."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post('/api/v1/integrations/sync/', {})
        assert response.status_code == 400

    def test_simulate_webhook_action(self):
        """La acción simulate-webhook debe crear un nuevo log en base de datos."""
        self.client.force_authenticate(user=self.admin_user)
        payload = {"amount": 500.00}
        response = self.client.post('/api/v1/integrations/simulate-webhook/', payload)
        assert response.status_code == 200
        assert float(response.data['amount']) == 500.00
        
        log = BankSyncLog.objects.get(id=response.data['id'])
        assert log.amount == 500.00
        assert "STP-" in log.external_id

    @patch('stripe.checkout.Session.create')
    def test_stripe_provider_create_checkout_session(self, mock_session_create):
        """Verifica la creación del enlace de checkout de Stripe y el registro del ID de sesión."""
        # Configurar mock de la sesión de Stripe
        mock_session = MagicMock()
        mock_session.id = "cs_test_999"
        mock_session.url = "https://checkout.stripe.mock/pay"
        mock_session_create.return_value = mock_session
        
        url = StripeProvider.create_checkout_session(self.order, "http://success", "http://cancel")
        
        assert url == "https://checkout.stripe.mock/pay"
        transaction = PaymentTransaction.objects.get(order=self.order)
        assert transaction.stripe_checkout_id == "cs_test_999"
        assert transaction.provider == "Stripe"

    @patch('stripe.Webhook.construct_event')
    def test_stripe_webhook_view_completed(self, mock_construct_event):
        """Verifica que el procesamiento de webhooks de Stripe complete la orden y active el despliegue."""
        # 1. Simular la transacción inicial (stripe_checkout_id ya en base de datos)
        PaymentTransaction.objects.create(
            order=self.order,
            stripe_checkout_id="cs_test_888",
            provider="Stripe",
            success=False
        )

        # 2. Configurar mock del evento de webhook
        mock_event = {
            'type': 'checkout.session.completed',
            'data': {
                'object': {
                    'id': 'cs_test_888',
                    'payment_intent': 'pi_test_intent_123',
                    'metadata': {
                        'order_id': self.order.id
                    }
                }
            }
        }
        mock_construct_event.return_value = mock_event
        
        # 3. Lanzar petición POST al webhook de Stripe
        response = self.client.post(
            '/api/v1/stripe-webhook/',
            data="{}",
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE="t=123,v1=abc"
        )
        assert response.status_code == 200
        
        # 4. Validar actualización de la orden, transacción y despliegue
        self.order.refresh_from_db()
        self.deployment.refresh_from_db()
        transaction = PaymentTransaction.objects.get(order=self.order)
        
        assert self.order.status == Order.StatusChoices.COMPLETED
        assert self.deployment.is_paid is True
        assert self.deployment.status == Deployment.StatusChoices.LIVE
        assert transaction.success is True
        assert transaction.stripe_payment_intent_id == "pi_test_intent_123"
