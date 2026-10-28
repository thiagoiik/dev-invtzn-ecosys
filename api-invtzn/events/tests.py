import pytest
import datetime
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from events.models import EventContext
from profiles.models import UserProfile

User = get_user_model()

@pytest.mark.django_db
class TestEvents:
    def setup_method(self):
        self.client = APIClient()

        # 1. Crear usuarios y perfiles
        self.user_a = User.objects.create_user(username='user_a', password='password123')
        self.profile_a = UserProfile.objects.create(remote_auth_id=self.user_a.id, custom_role=UserProfile.Role.CLIENT)

        self.user_b = User.objects.create_user(username='user_b', password='password123')
        self.profile_b = UserProfile.objects.create(remote_auth_id=self.user_b.id, custom_role=UserProfile.Role.CLIENT)

        # 2. Crear evento para el usuario A
        self.event_a = EventContext.objects.create(
            user=self.profile_a,
            title="Boda de Martha y Pekas",
            event_type="BODA",
            main_date=datetime.date(2026, 6, 15),
            location_name="Hacienda Sol"
        )

    def test_event_model_representation(self):
        """Verifica la representación del string en el modelo EventContext."""
        assert str(self.event_a) == "Boda de Martha y Pekas - 2026-06-15"

    def test_event_queryset_isolation_user_a(self):
        """El usuario A solo debe ver su propio evento."""
        self.client.force_authenticate(user=self.user_a)
        response = self.client.get('/api/v1/events/')
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['title'] == "Boda de Martha y Pekas"

    def test_event_queryset_isolation_user_b(self):
        """El usuario B no debe ver los eventos del usuario A."""
        self.client.force_authenticate(user=self.user_b)
        response = self.client.get('/api/v1/events/')
        assert response.status_code == 200
        assert len(response.data) == 0

    def test_event_retrieve_isolation_user_b(self):
        """El usuario B no debe poder consultar el evento del usuario A directamente."""
        self.client.force_authenticate(user=self.user_b)
        response = self.client.get(f'/api/v1/events/{self.event_a.id}/')
        assert response.status_code == 404

    def test_event_update_isolation_user_b(self):
        """El usuario B no debe poder actualizar el evento del usuario A."""
        self.client.force_authenticate(user=self.user_b)
        payload = {"title": "Boda Editada"}
        response = self.client.patch(f'/api/v1/events/{self.event_a.id}/', payload)
        assert response.status_code == 404

    def test_event_delete_isolation_user_b(self):
        """El usuario B no debe poder eliminar el evento del usuario A."""
        self.client.force_authenticate(user=self.user_b)
        response = self.client.delete(f'/api/v1/events/{self.event_a.id}/')
        assert response.status_code == 404

    def test_event_creation_sets_authenticated_user(self):
        """Verifica que la creación asocie el evento al usuario autenticado automáticamente."""
        self.client.force_authenticate(user=self.user_b)
        payload = {
            "title": "Bautizo de Sofia",
            "event_type": "BAUTIZO",
            "main_date": "2026-08-20",
            "location_name": "Salon Infantil"
        }
        response = self.client.post('/api/v1/events/', payload)
        assert response.status_code == 201
        
        # Validar base de datos
        event = EventContext.objects.get(title="Bautizo de Sofia")
        assert event.user.remote_auth_id == self.profile_b.remote_auth_id

    def test_event_creation_ignores_explicit_user(self):
        """Verifica que si se envía un 'user' explícito en el payload, sea ignorado/protegido."""
        self.client.force_authenticate(user=self.user_b)
        payload = {
            "title": "Fiesta de Graduacion",
            "event_type": "GRADUACION",
            "main_date": "2026-10-10",
            "user": self.profile_a.remote_auth_id  # Intentando asociarlo a User A
        }
        response = self.client.post('/api/v1/events/', payload)
        assert response.status_code == 201
        
        event = EventContext.objects.get(title="Fiesta de Graduacion")
        assert event.user.remote_auth_id == self.profile_b.remote_auth_id  # Debe seguir siendo User B
