import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from sales.models import Order, PaymentTransaction
from inventory.models import Product
from profiles.models import UserProfile

User = get_user_model()

@pytest.mark.django_db
class TestSales:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser2', password='password123')
        UserProfile.objects.create(remote_auth_id=self.user.id, custom_role=UserProfile.Role.CLIENT)
        self.product = Product.objects.create(name='Test Product 2', base_price=50.00, product_type='DIGITAL')
        self.client.force_authenticate(user=self.user)

    def test_create_order_model(self):
        order = Order.objects.create(
            user=self.user.id,
            product=self.product,
            total_amount=50.00,
            status=Order.StatusChoices.PENDING
        )
        assert order.user == self.user.id
        assert order.total_amount == 50.00
        assert order.status == 'PENDING'

        payment = PaymentTransaction.objects.create(
            order=order,
            provider='Stripe',
            transaction_id='txn_123',
            success=True
        )
        assert payment.order == order
        assert payment.success is True

    def test_order_viewset_list(self):
        Order.objects.create(user=self.user.id, product=self.product, total_amount=10.00)
        response = self.client.get('/api/v1/orders/')
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_order_viewset_create(self):
        payload = {
            'product': self.product.id,
            'total_amount': 25.00
        }
        response = self.client.post('/api/v1/orders/', payload)
        assert response.status_code == 201
        assert response.data['user'] == self.user.id
        assert float(response.data['total_amount']) == 25.00
        assert Order.objects.count() == 1

@pytest.mark.django_db
class TestPOSAndCashSessions:
    def setup_method(self):
        from inventory.models import Store
        from decimal import Decimal

        self.client = APIClient()
        self.product = Product.objects.create(name='Test Invitation POS', base_price=100.00, product_type='DIGITAL')

        # Vendedor y Admin
        self.vendor_user = User.objects.create_user(username='vendor1', password='password123')
        self.store = Store.objects.create(name='Sucursal Centro')
        self.vendor_profile = UserProfile.objects.create(
            remote_auth_id=self.vendor_user.id,
            custom_role=UserProfile.Role.VENDOR,
            assigned_store=self.store,
            base_commission_rate=Decimal('10.00')
        )

        self.client_user = User.objects.create_user(username='client1', password='password123')
        self.client_profile = UserProfile.objects.create(
            remote_auth_id=self.client_user.id,
            custom_role=UserProfile.Role.CLIENT
        )

    def test_complete_pos_order_success_cash(self):
        from sales.models import CashSession
        
        # 1. Crear sesión de caja abierta para el vendedor
        CashSession.objects.create(
            user=self.vendor_user.id,
            store=self.store,
            opening_balance=200.00,
            is_open=True
        )

        # 2. Crear orden pendiente vía API
        self.client.force_authenticate(user=self.vendor_user)
        payload = {
            'product': self.product.id,
            'total_amount': 100.00,
            'user': self.client_user.id
        }
        res_create = self.client.post('/api/v1/orders/', payload)
        assert res_create.status_code == 201
        order_id = res_create.data['id']

        response = self.client.post(f'/api/v1/orders/{order_id}/complete-pos/', {'payment_method': 'CASH'})
        
        assert response.status_code == 200
        order = Order.objects.get(id=order_id)
        assert order.status == Order.StatusChoices.COMPLETED
        assert order.payment.success is True
        assert order.payment.payment_method == 'CASH'
        assert order.commission.amount == 10.00 # 10% commission of 100.00

    def test_complete_pos_order_success_card_no_session_needed(self):
        self.client.force_authenticate(user=self.vendor_user)
        payload = {
            'product': self.product.id,
            'total_amount': 100.00,
            'user': self.client_user.id
        }
        res_create = self.client.post('/api/v1/orders/', payload)
        assert res_create.status_code == 201
        order_id = res_create.data['id']

        response = self.client.post(f'/api/v1/orders/{order_id}/complete-pos/', {'payment_method': 'CARD'})
        
        assert response.status_code == 200
        order = Order.objects.get(id=order_id)
        assert order.status == Order.StatusChoices.COMPLETED
        assert order.payment.success is True
        assert order.payment.payment_method == 'CARD'

    def test_complete_pos_order_fails_without_session(self):
        self.client.force_authenticate(user=self.vendor_user)
        payload = {
            'product': self.product.id,
            'total_amount': 100.00,
            'user': self.client_user.id
        }
        res_create = self.client.post('/api/v1/orders/', payload)
        assert res_create.status_code == 201
        order_id = res_create.data['id']

        response = self.client.post(f'/api/v1/orders/{order_id}/complete-pos/', {'payment_method': 'CASH'})
        
        assert response.status_code == 400
        assert 'Debes abrir un turno de caja' in response.data['error']

    def test_complete_pos_order_forbidden_for_client(self):
        # El vendedor crea la orden
        self.client.force_authenticate(user=self.vendor_user)
        payload = {
            'product': self.product.id,
            'total_amount': 100.00,
            'user': self.client_user.id
        }
        res_create = self.client.post('/api/v1/orders/', payload)
        assert res_create.status_code == 201
        order_id = res_create.data['id']

        # El cliente intenta completarla
        self.client.force_authenticate(user=self.client_user)
        response = self.client.post(f'/api/v1/orders/{order_id}/complete-pos/', {'payment_method': 'CASH'})
        
        assert response.status_code == 403
        assert 'No tienes permisos' in response.data['error']

    def test_cash_session_expected_balance_calculation(self):
        from sales.models import CashSession
        
        # 1. Crear sesión de caja abierta con $200
        session = CashSession.objects.create(
            user=self.vendor_user.id,
            store=self.store,
            opening_balance=200.00,
            is_open=True
        )

        # 2. Crear y completar orden por $100
        self.client.force_authenticate(user=self.vendor_user)
        payload = {
            'product': self.product.id,
            'total_amount': 100.00,
            'user': self.client_user.id
        }
        res_create = self.client.post('/api/v1/orders/', payload)
        assert res_create.status_code == 201
        order_id = res_create.data['id']

        res_comp = self.client.post(f'/api/v1/orders/{order_id}/complete-pos/', {'payment_method': 'CASH'})
        assert res_comp.status_code == 200

        # 3. Cerrar sesión reportando $300 reales
        res_close = self.client.post(f'/api/v1/cash-sessions/{session.id}/close/', {'closing_balance': 300.00})
        assert res_close.status_code == 200
        
        assert float(res_close.data['total_sales_amount']) == 100.00
        assert float(res_close.data['expected_closing_balance']) == 300.00
        assert float(res_close.data['difference']) == 0.00
        assert res_close.data['is_open'] is False


@pytest.mark.django_db
class TestStage2Features:
    def setup_method(self):
        from inventory.models import Store
        from decimal import Decimal

        self.client = APIClient()
        self.p1 = Product.objects.create(name='Boda Oro', base_price=100.00, product_type='DIGITAL')
        self.p2 = Product.objects.create(name='Boda Plata', base_price=50.00, product_type='DIGITAL')

        # Admin, Franchisee, and Vendor Users
        self.admin_user = User.objects.create_user(username='admin_test', password='password123')
        self.admin_profile = UserProfile.objects.create(
            remote_auth_id=self.admin_user.id,
            custom_role=UserProfile.Role.ADMIN
        )

        self.franchisee_user = User.objects.create_user(username='fran_test', password='password123')
        self.franchisee_profile = UserProfile.objects.create(
            remote_auth_id=self.franchisee_user.id,
            custom_role=UserProfile.Role.FRANCHISEE
        )

        self.vendor_user = User.objects.create_user(username='vendor_test', password='password123')
        self.vendor_profile = UserProfile.objects.create(
            remote_auth_id=self.vendor_user.id,
            custom_role=UserProfile.Role.VENDOR
        )

        self.client_user = User.objects.create_user(username='client_test', password='password123')
        self.client_profile = UserProfile.objects.create(
            remote_auth_id=self.client_user.id,
            custom_role=UserProfile.Role.CLIENT
        )

    def test_create_order_with_items(self):
        self.client.force_authenticate(user=self.admin_user)
        payload = {
            'total_amount': 150.00,
            'subtotal_amount': 150.00,
            'user': self.client_user.id,
            'items': [
                {'product': self.p1.id, 'quantity': 1, 'price_at_sale': 100.00},
                {'product': self.p2.id, 'quantity': 1, 'price_at_sale': 50.00}
            ]
        }
        response = self.client.post('/api/v1/orders/', payload, format='json')
        assert response.status_code == 201
        order_id = response.data['id']
        order = Order.objects.get(id=order_id)
        assert order.items.count() == 2
        # Backwards compatibility: the primary product on the order should point to the first item's product
        assert order.product == self.p1

    def test_discount_allowed_for_admin_and_franchisee(self):
        # Admin
        self.client.force_authenticate(user=self.admin_user)
        payload = {
            'product': self.p1.id,
            'total_amount': 90.00,
            'subtotal_amount': 100.00,
            'discount_amount': 10.00,
            'user': self.client_user.id
        }
        response = self.client.post('/api/v1/orders/', payload)
        assert response.status_code == 201

        # Franchisee
        self.client.force_authenticate(user=self.franchisee_user)
        payload = {
            'product': self.p1.id,
            'total_amount': 80.00,
            'subtotal_amount': 100.00,
            'discount_amount': 20.00,
            'user': self.client_user.id
        }
        response = self.client.post('/api/v1/orders/', payload)
        assert response.status_code == 201

    def test_discount_forbidden_for_vendor_and_client(self):
        # Vendor
        self.client.force_authenticate(user=self.vendor_test if hasattr(self, 'vendor_test') else self.vendor_user)
        payload = {
            'product': self.p1.id,
            'total_amount': 90.00,
            'subtotal_amount': 100.00,
            'discount_amount': 10.00,
            'user': self.client_user.id
        }
        response = self.client.post('/api/v1/orders/', payload)
        assert response.status_code == 400
        assert 'discount_amount' in response.data
        assert 'No tienes permisos' in response.data['discount_amount'][0]

        # Client
        self.client.force_authenticate(user=self.client_user)
        payload = {
            'product': self.p1.id,
            'total_amount': 90.00,
            'subtotal_amount': 100.00,
            'discount_amount': 10.00,
        }
        response = self.client.post('/api/v1/orders/', payload)
        assert response.status_code == 400
        assert 'discount_amount' in response.data


