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
            user=self.user.id,
            product=self.product,
            status=Deployment.StatusChoices.DRAFT,
            slug='test-slug'
        )
        assert deployment.user == self.user.id
        assert deployment.product == self.product
        assert deployment.status == 'DRAFT'
        assert deployment.slug == 'test-slug'
        assert str(deployment) == f"test-slug - User {self.user.id} (DRAFT)"

    def test_deployment_viewset_list(self):
        Deployment.objects.create(user=self.user.id, product=self.product)
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
        Deployment.objects.create(user=other_user.id, product=self.product)
        response = self.client.get('/api/v1/deployments/')
        assert response.status_code == 200
        assert len(response.data) == 0

    def test_vendor_cannot_patch_deployment(self):
        vendor_user = User.objects.create_user(username='vendor', password='password123')
        UserProfile.objects.create(remote_auth_id=vendor_user.id, custom_role=UserProfile.Role.VENDOR)
        deployment = Deployment.objects.create(user=self.user.id, vendor_id=vendor_user.id, product=self.product)
        self.client.force_authenticate(user=vendor_user)
        response = self.client.patch(f'/api/v1/deployments/{deployment.id}/', {'slug': 'hacked'})
        assert response.status_code == 403

    def test_designer_can_patch_deployment(self):
        designer_user = User.objects.create_user(username='designer', password='password123')
        UserProfile.objects.create(remote_auth_id=designer_user.id, custom_role=UserProfile.Role.DESIGNER)
        deployment = Deployment.objects.create(user=self.user.id, product=self.product)
        self.client.force_authenticate(user=designer_user)
        response = self.client.patch(f'/api/v1/deployments/{deployment.id}/', {'slug': 'fixed'})
        assert response.status_code == 200
        deployment.refresh_from_db()
        assert deployment.slug == 'fixed'

    def test_open_graph_unpaid_deployment(self):
        deployment = Deployment.objects.create(
            user=self.user.id,
            product=self.product,
            is_paid=False,
            slug='test-unpaid-og',
            custom_data={'event_title': 'Boda de Laura y Carlos'}
        )
        response = self.client.get(f'/api/v1/deployments/og/{deployment.slug}/')
        assert response.status_code == 200
        html = response.content.decode('utf-8')
        assert 'og:title' in html
        assert 'Invitación: Boda de Laura y Carlos' in html
        assert 'og-free-banner.png' in html

    def test_open_graph_paid_deployment_custom(self):
        custom_data = {
            'og_title': 'Gran Boda Real',
            'og_description': 'Ven a celebrar con nosotros',
            'og_image': 'https://example.com/invitation.jpg'
        }
        deployment = Deployment.objects.create(
            user=self.user.id,
            product=self.product,
            is_paid=True,
            slug='test-paid-og',
            custom_data=custom_data
        )
        response = self.client.get(f'/api/v1/deployments/og/{deployment.slug}/')
        assert response.status_code == 200
        html = response.content.decode('utf-8')
        assert 'Gran Boda Real' in html
        assert 'Ven a celebrar con nosotros' in html
        assert 'https://example.com/invitation.jpg' in html

    def test_public_metric_registration(self):
        deployment = Deployment.objects.create(
            user=self.user.id,
            product=self.product,
            slug='test-metrics-slug'
        )
        # Log out user to simulate anonymous public traffic
        self.client.force_authenticate(user=None)
        
        payload = {'metric_type': 'VISIT'}
        # Custom user agent and client IP
        response = self.client.post(
            f'/api/v1/deployments/slug/{deployment.slug}/metric/',
            payload,
            HTTP_USER_AGENT='Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1',
            REMOTE_ADDR='192.168.1.50'
        )
        assert response.status_code == 200
        assert response.data['success'] == 'Métrica registrada'
        
        # Verify db record
        from deployments.models import DeploymentMetric
        metric = DeploymentMetric.objects.filter(deployment=deployment).first()
        assert metric is not None
        assert metric.metric_type == 'VISIT'
        assert metric.ip_address == '192.168.1.50'
        assert 'iPhone' in metric.user_agent
        # Localhost/private IP defaults to México / Localhost in the mock
        assert metric.country == 'México'
        assert metric.city == 'Localhost'

    def test_get_metrics_authorization(self):
        deployment = Deployment.objects.create(
            user=self.user.id,
            product=self.product,
            slug='auth-metrics-slug'
        )
        # Test 1: Owner gets access
        response = self.client.get(f'/api/v1/deployments/{deployment.id}/metrics/')
        assert response.status_code == 200

        # Test 2: Unauthenticated user gets 401 or 403
        self.client.force_authenticate(user=None)
        response = self.client.get(f'/api/v1/deployments/{deployment.id}/metrics/')
        assert response.status_code in [401, 403]

        # Test 3: Other authenticated client gets 403 or 404
        other_user = User.objects.create_user(username='other_client', password='password123')
        UserProfile.objects.create(remote_auth_id=other_user.id, custom_role=UserProfile.Role.CLIENT)
        self.client.force_authenticate(user=other_user)
        response = self.client.get(f'/api/v1/deployments/{deployment.id}/metrics/')
        assert response.status_code in [403, 404]

        # Test 4: Admin gets access
        admin_user = User.objects.create_user(username='admin_user', password='password123')
        UserProfile.objects.create(remote_auth_id=admin_user.id, custom_role=UserProfile.Role.ADMIN)
        self.client.force_authenticate(user=admin_user)
        response = self.client.get(f'/api/v1/deployments/{deployment.id}/metrics/')
        assert response.status_code == 200

    def test_get_metrics_aggregations_and_ip_masking(self):
        deployment = Deployment.objects.create(
            user=self.user.id,
            product=self.product,
            slug='agg-metrics-slug'
        )
        from deployments.models import DeploymentMetric
        
        # Seed metrics (1 Mobile Safari, 1 Desktop Chrome)
        DeploymentMetric.objects.create(
            deployment=deployment,
            metric_type='VISIT',
            ip_address='189.120.45.67',
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) Version/16.5 Mobile/15E148 Safari/604.1',
            country='México',
            city='Guadalajara'
        )
        DeploymentMetric.objects.create(
            deployment=deployment,
            metric_type='VISIT',
            ip_address='8.8.8.8',
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/113.0.0.0 Safari/537.36',
            country='United States',
            city='Mountain View'
        )
        # Seed RSVP
        DeploymentMetric.objects.create(
            deployment=deployment,
            metric_type='RSVP_SUBMIT',
            ip_address='8.8.8.8',
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/113.0.0.0 Safari/537.36',
            country='United States',
            city='Mountain View'
        )
        
        response = self.client.get(f'/api/v1/deployments/{deployment.id}/metrics/')
        assert response.status_code == 200
        
        data = response.data
        assert data['summary']['total_visits'] == 2
        assert data['summary']['total_rsvps'] == 1
        assert data['summary']['rsvp_rate'] == 50.0
        
        # Verify IP masking
        recent_logs = data['recent']
        assert len(recent_logs) == 3
        # e.g. 189.120.45.67 -> 189.120.*.*
        masked_ips = [r['ip_address'] for r in recent_logs]
        assert '189.120.*.*' in masked_ips
        assert '8.8.*.*' in masked_ips
        assert '8.8.8.8' not in masked_ips
        
        # Verify browser / device aggregation
        devices = {d['device']: d['count'] for d in data['by_device']}
        browsers = {b['browser']: b['count'] for b in data['by_browser']}
        
        assert devices['Móvil'] == 1
        assert devices['Escritorio'] == 2 # 1 VISIT + 1 RSVP_SUBMIT
        assert browsers['Safari'] == 1
        assert browsers['Chrome'] == 2

