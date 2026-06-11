import pytest
from unittest import mock
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
        assert response.status_code == 202
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

    def test_record_metric_task_internal_logic(self):
        from deployments.tasks import record_metric_task
        from deployments.models import DeploymentMetric
        import unittest.mock as mock

        deployment = Deployment.objects.create(
            user=self.user.id,
            product=self.product,
            slug='test-task-slug'
        )

        # 1. Test local IP bypass (Docker 172.16.x.x)
        record_metric_task(deployment.id, 'VISIT', '172.18.0.2', 'Mozilla/5.0')
        metric = DeploymentMetric.objects.filter(deployment=deployment, ip_address='172.18.0.2').first()
        assert metric is not None
        assert metric.city == 'Localhost'
        assert metric.country == 'México'

        # 2. Test fallback to ip-api.com (when GEOIP_DATABASE_PATH is unset/invalid)
        with mock.patch('requests.get') as mock_get:
            mock_res = mock.Mock()
            mock_res.json.return_value = {
                'status': 'success',
                'city': 'Santiago',
                'country': 'Chile'
            }
            mock_get.return_value = mock_res

            # Ensure env var is empty/non-existent path
            with mock.patch.dict('os.environ', {'GEOIP_DATABASE_PATH': ''}):
                record_metric_task(deployment.id, 'VISIT', '200.1.2.3', 'Mozilla/5.0')

            metric_fallback = DeploymentMetric.objects.filter(deployment=deployment, ip_address='200.1.2.3').first()
            assert metric_fallback is not None
            assert metric_fallback.city == 'Santiago'
            assert metric_fallback.country == 'Chile'
            mock_get.assert_called_once_with('http://ip-api.com/json/200.1.2.3', timeout=2.0)

        # 3. Test MaxMind local DB resolution
        with mock.patch('os.path.exists', return_value=True):
            with mock.patch.dict('os.environ', {'GEOIP_DATABASE_PATH': '/dummy/path/GeoLite2-City.mmdb'}):
                with mock.patch('geoip2.database.Reader') as mock_reader_cls:
                    mock_reader = mock.MagicMock()
                    mock_reader_cls.return_value.__enter__.return_value = mock_reader
                    
                    mock_response = mock.Mock()
                    mock_response.country.names = {'es': 'España'}
                    mock_response.city.names = {'es': 'Madrid'}
                    mock_reader.city.return_value = mock_response

                    record_metric_task(deployment.id, 'VISIT', '8.8.8.8', 'Mozilla/5.0')

                    metric_local = DeploymentMetric.objects.filter(deployment=deployment, ip_address='8.8.8.8').first()
                    assert metric_local is not None
                    assert metric_local.city == 'Madrid'
                    assert metric_local.country == 'España'

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

    def test_creation_mode_default(self):
        deployment = Deployment.objects.create(
            user=self.user.id,
            product=self.product,
            status=Deployment.StatusChoices.DRAFT,
            slug='test-mode-slug'
        )
        assert deployment.creation_mode == Deployment.CreationMode.CANVAS

    def test_slug_regex_validation(self):
        # 1. Valid slug
        payload = {
            'product': self.product.id,
            'slug': 'valid-slug-123'
        }
        response = self.client.post('/api/v1/deployments/', payload)
        assert response.status_code == 201

        # 2. Invalid slug
        payload['slug'] = 'invalid_slug_with_under'
        response = self.client.post('/api/v1/deployments/', payload)
        assert response.status_code == 400
        assert 'slug' in response.data or 'non_field_errors' in response.data

        # 3. Invalid slug with spaces
        payload['slug'] = 'invalid slug space'
        response = self.client.post('/api/v1/deployments/', payload)
        assert response.status_code == 400

        # 4. Invalid slug with capitals
        payload['slug'] = 'Invalid-Slug'
        response = self.client.post('/api/v1/deployments/', payload)
        assert response.status_code == 400

    def test_client_can_modify_catalog_deployment_data(self):
        catalog_deployment = Deployment.objects.create(
            user=self.user.id,
            product=self.product,
            slug='catalog-deployment',
            creation_mode=Deployment.CreationMode.CATALOG,
            custom_data={'cover': {'title': 'original'}}
        )
        # Client tries to update custom_data
        response = self.client.patch(f'/api/v1/deployments/{catalog_deployment.id}/', {'custom_data': {'cover': {'title': 'changed'}}}, format='json')
        assert response.status_code == 200
        catalog_deployment.refresh_from_db()
        assert catalog_deployment.custom_data['cover']['title'] == 'changed'

        # Designer tries to update custom_data (should succeed)
        designer_user = User.objects.create_user(username='designer_user_2', password='password123')
        UserProfile.objects.create(remote_auth_id=designer_user.id, custom_role=UserProfile.Role.DESIGNER)
        self.client.force_authenticate(user=designer_user)
        response = self.client.patch(f'/api/v1/deployments/{catalog_deployment.id}/', {'custom_data': {'key': 'changed'}}, format='json')
        assert response.status_code == 200

    def test_system_logs_permissions(self):
        # Unauthenticated
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/v1/system-logs/')
        assert response.status_code in [401, 403]

        # Authenticated Client
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/v1/system-logs/')
        assert response.status_code == 403

        # Authenticated Admin
        admin_user = User.objects.create_user(username='admin_user_logs', password='password123')
        UserProfile.objects.create(remote_auth_id=admin_user.id, custom_role=UserProfile.Role.ADMIN)
        self.client.force_authenticate(user=admin_user)
        response = self.client.get('/api/v1/system-logs/')
        assert response.status_code == 200

    def test_order_completion_triggers_signal_and_logs(self):
        from sales.models import Order, OrderItem
        from deployments.models import SystemLog

        # Create another product to change to
        new_product = Product.objects.create(name='Premium Product', base_price=50.00, product_type='DIGITAL', tier_level='PREMIUM')

        deployment = Deployment.objects.create(
            user=self.user.id,
            product=self.product,
            slug='test-signal-slug',
            creation_mode=Deployment.CreationMode.CANVAS
        )

        order = Order.objects.create(
            user=self.user.id,
            deployment=deployment,
            total_amount=50.00,
            status=Order.StatusChoices.PENDING
        )
        OrderItem.objects.create(order=order, product=new_product, quantity=1, price_at_sale=50.00)

        # Clear existing logs if any
        SystemLog.objects.all().delete()

        # Simulate completion
        order.status = Order.StatusChoices.COMPLETED
        order.save()

        # Check deployment has new product and is active/paid
        deployment.refresh_from_db()
        assert deployment.product == new_product
        assert deployment.status == Deployment.StatusChoices.LIVE
        assert deployment.is_paid is True

        # Check SystemLog entries
        logs = SystemLog.objects.all()
        assert logs.count() == 2

        # One should be DEPLOYMENT_STATE, another PAYMENT_FLOW
        log_types = [log.log_type for log in logs]
        assert 'DEPLOYMENT_STATE' in log_types
        assert 'PAYMENT_FLOW' in log_types

        # Verify details
        state_log = logs.filter(log_type='DEPLOYMENT_STATE').first()
        assert state_log.user_id == self.user.id
        assert state_log.metadata['deployment_id'] == deployment.id
        assert state_log.metadata['product_id'] == new_product.id

    def test_create_deployment_clones_template_data(self):
        # 1. Create a master template deployment
        template_dep = Deployment.objects.create(
            user=None,
            product=self.product,
            status=Deployment.StatusChoices.LIVE,
            slug='master-template-123',
            creation_mode=Deployment.CreationMode.CATALOG,
            custom_data={'cover': {'title': 'Boda Master', 'date': '2026-12-25'}}
        )

        # 2. Update our product to point to this template_slug
        self.product.template_slug = 'master-template-123'
        self.product.save()

        # 3. Create a new deployment for this product (with empty custom_data)
        new_dep = Deployment.objects.create(
            user=self.user.id,
            product=self.product,
            status=Deployment.StatusChoices.DRAFT,
            custom_data={}
        )

        # 4. Check if the new deployment cloned the custom_data and creation_mode
        assert new_dep.custom_data == template_dep.custom_data
        assert new_dep.creation_mode == template_dep.creation_mode

        # 5. Create another deployment with the default frontend placeholder custom_data
        default_placeholder = {"message": "¡Diseña tu invitación aquí!", "theme": "light"}
        placeholder_dep = Deployment.objects.create(
            user=self.user.id,
            product=self.product,
            status=Deployment.StatusChoices.DRAFT,
            custom_data=default_placeholder
        )

        # 6. Check if it successfully cloned custom_data and creation_mode as well
        assert placeholder_dep.custom_data == template_dep.custom_data
        assert placeholder_dep.creation_mode == template_dep.creation_mode

        # 7. Create another deployment with customized cover titles (like the QuickDraftModal flow)
        custom_input = {
            "cover": {"title": "Ana & Luis", "date": "25 DE DICIEMBRE DE 2026"},
            "rsvp": {"eventTitle": "Ana & Luis"}
        }
        merged_dep = Deployment.objects.create(
            user=self.user.id,
            product=self.product,
            status=Deployment.StatusChoices.DRAFT,
            custom_data=custom_input
        )

        # 8. Check that it successfully cloned layout fields but merged the customized inputs
        assert merged_dep.custom_data["cover"]["title"] == "Ana & Luis"
        assert merged_dep.custom_data["cover"]["date"] == "25 DE DICIEMBRE DE 2026"
        assert merged_dep.custom_data["rsvp"]["eventTitle"] == "Ana & Luis"
        assert merged_dep.creation_mode == template_dep.creation_mode

    def test_deployment_allowed_features_by_tier(self):
        # 1. Test Premium Tier
        premium_prod = Product.objects.create(name='Premium Product', base_price=30.00, product_type='DIGITAL', tier_level='PREMIUM')
        premium_dep = Deployment.objects.create(user=self.user.id, product=premium_prod)
        assert premium_dep.allowed_features['gift_table'] is True
        assert premium_dep.allowed_features['photo_carousel'] is True

        # 2. Test Standard Tier
        standard_prod = Product.objects.create(name='Standard Product', base_price=20.00, product_type='DIGITAL', tier_level='STANDARD')
        standard_dep = Deployment.objects.create(user=self.user.id, product=standard_prod)
        assert standard_dep.allowed_features['gift_table'] is False
        assert standard_dep.allowed_features['photo_carousel'] is False

        # 3. Test Basic Tier
        basic_prod = Product.objects.create(name='Basic Product', base_price=0.00, product_type='DIGITAL', tier_level='BASIC')
        basic_dep = Deployment.objects.create(user=self.user.id, product=basic_prod)
        assert basic_dep.allowed_features['gift_table'] is False
        assert basic_dep.allowed_features['photo_carousel'] is False

    @mock.patch('requests.get')
    def test_unsplash_search_proxy(self, mock_get):
        from unittest import mock
        class MockResponse:
            status_code = 200
            def json(self):
                return {
                    "total": 1,
                    "total_pages": 1,
                    "results": [
                        {
                            "id": "img123",
                            "urls": {
                                "regular": "http://regular.url",
                                "small": "http://small.url"
                            },
                            "user": {
                                "name": "Test Photographer",
                                "links": {
                                    "html": "http://unsplash-user.url"
                                }
                            }
                        }
                    ]
                }
        
        mock_get.return_value = MockResponse()

        response = self.client.get('/api/v1/deployments/unsplash-search/?query=wedding')
        assert response.status_code == 200
        assert response.data['total'] == 1
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['id'] == 'img123'
        assert response.data['results'][0]['url'] == 'http://regular.url'
        assert response.data['results'][0]['author'] == 'Test Photographer'
        
        # Probar caso sin query
        response_empty = self.client.get('/api/v1/deployments/unsplash-search/')
        assert response_empty.status_code == 400

    @mock.patch('requests.get')
    def test_jamendo_search_proxy(self, mock_get):
        class MockResponse:
            status_code = 200
            def json(self):
                return {
                    "headers": {
                        "status": "success",
                        "code": 0
                    },
                    "results": [
                        {
                            "id": "track123",
                            "name": "Romantic Acoustic",
                            "duration": 180,
                            "artist_name": "Lovely Artist",
                            "album_image": "http://album.image/cover.jpg",
                            "audio": "http://jamendo.com/track123.mp3"
                        }
                    ]
                }
        
        mock_get.return_value = MockResponse()

        response = self.client.get('/api/v1/deployments/jamendo-search/?q=romantic')
        assert response.status_code == 200
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['id'] == 'track123'
        assert response.data['results'][0]['title'] == 'Romantic Acoustic'
        assert response.data['results'][0]['artist'] == 'Lovely Artist'
        assert response.data['results'][0]['duration'] == 180
        assert response.data['results'][0]['cover'] == 'http://album.image/cover.jpg'
        assert response.data['results'][0]['audio'] == 'http://jamendo.com/track123.mp3'
        
        # Probar caso sin parametro q
        response_empty = self.client.get('/api/v1/deployments/jamendo-search/')
        assert response_empty.status_code == 400

    def test_dynamic_blocks_validation_by_visibility(self):
        from inventory.models import Product
        product_basic = Product.objects.create(
            name="Basic Invitation",
            base_price=0.00,
            product_type=Product.ProductType.DIGITAL,
            tier_level=Product.TierLevel.BASIC
        )
        
        from rest_framework.test import APIClient
        client = APIClient()
        from django.contrib.auth.models import User as DjangoUser
        from profiles.models import UserProfile
        django_user = DjangoUser.objects.create_user(username="client_user_test", password="password")
        UserProfile.objects.create(remote_auth_id=django_user.id, custom_role="CLIENT")
        client.force_authenticate(user=django_user)

        deployment = Deployment.objects.create(
            product=product_basic,
            slug="test-validation-visibility",
            user=django_user.id
        )
        
        url = f'/api/v1/deployments/{deployment.id}/'
        
        # 1. Con visible: False (debería pasar en verde)
        data_inactive = {
            "custom_data": {
                "blocks": [
                    {"id": "timer", "type": "CountdownTimer", "visible": False}
                ]
            }
        }
        response = client.patch(url, data_inactive, format='json')
        assert response.status_code == 200, f"Debería permitir guardar bloques inactivos. Error: {response.data}"
        
        # 2. Con visible: True (debería fallar con 400 Bad Request)
        data_active = {
            "custom_data": {
                "blocks": [
                    {"id": "timer", "type": "CountdownTimer", "visible": True}
                ]
            }
        }
        response_active = client.patch(url, data_active, format='json')
        assert response_active.status_code == 400, "Debería rechazar bloques premium activos en plan básico."
        assert "CountdownTimer" in str(response_active.data['custom_data'][0])

    def test_designer_can_request_review_and_notify_admins(self):
        # 1. Create a designer user and a draft deployment
        designer_user = User.objects.create_user(username='designer_review_test', password='password123')
        UserProfile.objects.create(remote_auth_id=designer_user.id, custom_role=UserProfile.Role.DESIGNER)
        deployment = Deployment.objects.create(user=designer_user.id, product=self.product, status=Deployment.StatusChoices.DRAFT)
        
        # 2. Create some admins
        admin_user1 = User.objects.create_user(username='admin_review_test1', password='password123')
        UserProfile.objects.create(remote_auth_id=admin_user1.id, custom_role=UserProfile.Role.ADMIN)
        admin_user2 = User.objects.create_user(username='admin_review_test2', password='password123')
        UserProfile.objects.create(remote_auth_id=admin_user2.id, custom_role=UserProfile.Role.ADMIN)

        self.client.force_authenticate(user=designer_user)
        
        # 3. Call request-review action
        response = self.client.post(f'/api/v1/deployments/{deployment.id}/request-review/')
        assert response.status_code == 200
        assert response.data['success'] == 'Solicitud de revisión enviada al administrador exitosamente.'
        
        # 4. Check that system logs and communication logs are created
        from deployments.models import SystemLog
        assert SystemLog.objects.filter(log_type=SystemLog.LogType.USER_ACTION, user_id=designer_user.id).exists()
        
        from profiles.models import CommunicationLog
        # 2 logs should exist, one for each admin
        admin1_logs = CommunicationLog.objects.filter(user__remote_auth_id=admin_user1.id, channel=CommunicationLog.Channel.SYSTEM)
        admin2_logs = CommunicationLog.objects.filter(user__remote_auth_id=admin_user2.id, channel=CommunicationLog.Channel.SYSTEM)
        assert admin1_logs.count() == 1
        assert admin2_logs.count() == 1
        assert f"(ID: {deployment.id})" in admin1_logs.first().subject

    def test_publish_product_sets_status_to_active(self):
        # 1. Create an admin user and a draft deployment
        admin_user = User.objects.create_user(username='admin_publish_test', password='password123')
        UserProfile.objects.create(remote_auth_id=admin_user.id, custom_role=UserProfile.Role.ADMIN)
        deployment = Deployment.objects.create(user=self.user.id, product=self.product, status=Deployment.StatusChoices.DRAFT, slug='temp-publish-slug')
        
        self.client.force_authenticate(user=admin_user)
        
        # 2. Call publish-product action
        payload = {
            'name': 'Template Catalog Invitation',
            'slug': 'temp-publish-slug-new',
            'store_id': None
        }
        response = self.client.post(f'/api/v1/deployments/{deployment.id}/publish-product/', payload, format='json')
        assert response.status_code == 200
        
        # 3. Verify status in database is ACTIVE (not LIVE)
        deployment.refresh_from_db()
        assert deployment.status == Deployment.StatusChoices.ACTIVE
        assert deployment.slug == 'temp-publish-slug-new'




