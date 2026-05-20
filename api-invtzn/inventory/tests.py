import pytest
from unittest.mock import patch
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from inventory.models import Store, Product, Template
from profiles.models import UserProfile

User = get_user_model()

@pytest.mark.django_db
class TestInventory:
    def setup_method(self):
        self.client = APIClient()

        # 1. Crear usuarios y perfiles
        self.admin_user = User.objects.create_user(username='admin_usr', password='password123')
        self.admin_profile = UserProfile.objects.create(remote_auth_id=self.admin_user.id, custom_role=UserProfile.Role.ADMIN)

        self.franchisee_user = User.objects.create_user(username='fran_usr', password='password123')
        self.franchisee_profile = UserProfile.objects.create(remote_auth_id=self.franchisee_user.id, custom_role=UserProfile.Role.FRANCHISEE)

        self.manager_user = User.objects.create_user(username='mgr_usr', password='password123')
        self.manager_profile = UserProfile.objects.create(remote_auth_id=self.manager_user.id, custom_role=UserProfile.Role.MANAGER)

        self.unauthorized_user = User.objects.create_user(username='unauth_usr', password='password123')
        self.unauthorized_profile = UserProfile.objects.create(remote_auth_id=self.unauthorized_user.id, custom_role=UserProfile.Role.CLIENT)

        # 2. Crear datos de prueba (Tiendas)
        self.store_1 = Store.objects.create(name="Store Uno", city="CDMX", owner=self.franchisee_profile)
        self.store_2 = Store.objects.create(name="Store Dos", city="Monterrey", owner=self.admin_profile)

        # Asignar tienda al manager
        self.manager_profile.assigned_store = self.store_1
        self.manager_profile.save()

        # 3. Crear productos y plantillas
        self.product_digital = Product.objects.create(
            name="Digital Invitation", 
            base_price=150.00, 
            product_type=Product.ProductType.DIGITAL,
            has_template=True
        )
        self.template = Template.objects.create(
            product=self.product_digital,
            vue_component_name="ClassicBoda",
            default_config={"color": "gold", "font": "serif"}
        )

    def test_models_representation(self):
        """Verifica la correcta representación en cadena (__str__) de los modelos."""
        assert str(self.store_1) == "Store Uno (CDMX)"
        assert str(self.product_digital) == "Digital Invitation ($150.0)"
        assert str(self.template) == "Configuración para Digital Invitation"

    def test_product_viewset_list_public(self):
        """Verifica que cualquier usuario pueda ver el catálogo de productos activos."""
        response = self.client.get('/api/v1/products/')
        assert response.status_code == 200
        # Debe incluir a product_digital
        product_names = [p['name'] for p in response.data]
        assert "Digital Invitation" in product_names

    def test_store_viewset_queryset_admin(self):
        """Un administrador debe poder ver todas las tiendas del ecosistema."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/v1/stores/')
        assert response.status_code == 200
        assert len(response.data) == 2

    def test_store_viewset_queryset_franchisee(self):
        """Un franquiciatario solo debe poder ver las tiendas que posee."""
        self.client.force_authenticate(user=self.franchisee_user)
        response = self.client.get('/api/v1/stores/')
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['name'] == "Store Uno"

    def test_store_viewset_queryset_manager(self):
        """Un gerente solo debe poder ver la tienda a la que está asignado."""
        self.client.force_authenticate(user=self.manager_user)
        response = self.client.get('/api/v1/stores/')
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['name'] == "Store Uno"

    def test_store_viewset_queryset_client_none(self):
        """Un usuario cliente común (no staff) no ve ninguna tienda (vacío)."""
        self.client.force_authenticate(user=self.unauthorized_user)
        response = self.client.get('/api/v1/stores/')
        assert response.status_code == 200
        assert len(response.data) == 0

    def test_store_creation_franchisee_owner(self):
        """Al crear una tienda, si el usuario es franquiciatario, se le asigna como dueño automáticamente."""
        self.client.force_authenticate(user=self.franchisee_user)
        payload = {
            "name": "Store Tres",
            "city": "Guadalajara"
        }
        response = self.client.post('/api/v1/stores/', payload)
        assert response.status_code == 201
        
        # Consultamos la base de datos para validar el dueño
        store = Store.objects.get(name="Store Tres")
        assert store.owner.remote_auth_id == self.franchisee_profile.remote_auth_id

    @patch('integrations.stripe_provider.StripeProvider.create_onboarding_link')
    def test_store_stripe_onboarding_action(self, mock_create_link):
        """Verifica que la acción stripe-onboarding retorne correctamente el enlace mockeado."""
        mock_create_link.return_value = "https://stripe.mock/onboarding-link"
        self.client.force_authenticate(user=self.franchisee_user)
        
        payload = {
            "return_url": "http://return.url",
            "refresh_url": "http://refresh.url"
        }
        response = self.client.post(f'/api/v1/stores/{self.store_1.id}/stripe-onboarding/', payload)
        assert response.status_code == 200
        assert response.data['url'] == "https://stripe.mock/onboarding-link"
        mock_create_link.assert_called_once_with(self.store_1, "http://return.url", "http://refresh.url")

    @patch('integrations.stripe_provider.StripeProvider.check_onboarding_status')
    def test_store_stripe_verify_action(self, mock_check_status):
        """Verifica que la acción stripe-verify retorne correctamente el estado del onboarding."""
        mock_check_status.return_value = True
        self.store_1.stripe_account_id = "acct_test123"
        self.store_1.save()
        
        self.client.force_authenticate(user=self.franchisee_user)
        response = self.client.get(f'/api/v1/stores/{self.store_1.id}/stripe-verify/')
        assert response.status_code == 200
        assert response.data['stripe_onboarding_completed'] is True
        assert response.data['stripe_account_id'] == "acct_test123"
        mock_check_status.assert_called_once_with(self.store_1)
