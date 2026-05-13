import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from sales.models import Order, PaymentTransaction
from inventory.models import Product

User = get_user_model()

@pytest.mark.django_db
class TestSales:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser2', password='password123')
        self.product = Product.objects.create(name='Test Product 2', base_price=50.00, product_type='DIGITAL')
        self.client.force_authenticate(user=self.user)

    def test_create_order_model(self):
        order = Order.objects.create(
            user=self.user,
            product=self.product,
            total_amount=50.00,
            status=Order.StatusChoices.PENDING
        )
        assert order.user == self.user
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
        Order.objects.create(user=self.user, product=self.product, total_amount=10.00)
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
