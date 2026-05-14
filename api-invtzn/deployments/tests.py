import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from deployments.models import Deployment
from inventory.models import Product
from profiles.models import UserProfile

User = get_user_model()

@pytest.mark.django_db
class TestDeployments:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password123')
        UserProfile.objects.create(remote_auth_id=self.user.id, custom_role=UserProfile.Role.CLIENT)
        self.product = Product.objects.create(name='Test Product', base_price=10.00, product_type='DIGITAL')
        self.client.force_authenticate(user=self.user)

    def test_create_deployment_model(self):
        deployment = Deployment.objects.create(
            user=self.user,
            product=self.product,
            status=Deployment.StatusChoices.DRAFT,
            slug='test-slug'
        )
        assert deployment.user == self.user
        assert deployment.product == self.product
        assert deployment.status == 'DRAFT'
        assert deployment.slug == 'test-slug'
        assert str(deployment) == f"test-slug - testuser (DRAFT)"

    def test_deployment_viewset_list(self):
        Deployment.objects.create(user=self.user, product=self.product)
        response = self.client.get('/api/v1/deployments/')
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_deployment_viewset_create(self):
        payload = {
            'product': self.product.id,
            'status': 'DRAFT'
        }
        response = self.client.post('/api/v1/deployments/', payload)
        assert response.status_code == 201
        assert response.data['user'] == self.user.id
        assert Deployment.objects.count() == 1

    def test_client_cannot_see_global_deployments(self):
        other_user = User.objects.create_user(username='other', password='password123')
        Deployment.objects.create(user=other_user, product=self.product)
        response = self.client.get('/api/v1/deployments/')
        assert response.status_code == 200
        assert len(response.data) == 0

    def test_vendor_cannot_patch_deployment(self):
        vendor_user = User.objects.create_user(username='vendor', password='password123')
        UserProfile.objects.create(remote_auth_id=vendor_user.id, custom_role=UserProfile.Role.VENDOR)
        deployment = Deployment.objects.create(user=self.user, product=self.product)
        self.client.force_authenticate(user=vendor_user)
        response = self.client.patch(f'/api/v1/deployments/{deployment.id}/', {'slug': 'hacked'})
        assert response.status_code == 403

    def test_designer_can_patch_deployment(self):
        designer_user = User.objects.create_user(username='designer', password='password123')
        UserProfile.objects.create(remote_auth_id=designer_user.id, custom_role=UserProfile.Role.DESIGNER)
        deployment = Deployment.objects.create(user=self.user, product=self.product)
        self.client.force_authenticate(user=designer_user)
        response = self.client.patch(f'/api/v1/deployments/{deployment.id}/', {'slug': 'fixed'})
        assert response.status_code == 200
        deployment.refresh_from_db()
        assert deployment.slug == 'fixed'
