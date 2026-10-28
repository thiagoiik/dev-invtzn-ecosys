import pytest
from unittest.mock import patch
from django.test import RequestFactory
from rest_framework.test import APIClient
from core.adapters import CustomAccountAdapter

class DummyConfirmation:
    def __init__(self, key):
        self.key = key

class TestAuthService:
    def test_get_email_confirmation_url(self):
        """Verifica que la URL generada apunte al frontend en lugar de al backend."""
        adapter = CustomAccountAdapter()
        rf = RequestFactory()
        request = rf.get('/some-path/')
        
        dummy_confirm = DummyConfirmation(key="abc123confirm")
        url = adapter.get_email_confirmation_url(request, dummy_confirm)
        
        assert url == "http://front.auth.local/verify-email/abc123confirm/"

    def test_send_mail_intercepts_password_reset_url(self):
        """Verifica que la URL del enlace de recuperación en el correo apunte a front.auth.local."""
        adapter = CustomAccountAdapter()
        context = {
            'password_reset_url': 'http://api.auth.local/reset/123/abc/'
        }
        
        with patch('allauth.account.adapter.DefaultAccountAdapter.send_mail') as mock_super_send:
            adapter.send_mail(
                template_prefix='account/email/password_reset_key',
                email='user@example.com',
                context=context
            )
            # El contexto debe mutar en el lugar
            assert context['password_reset_url'] == 'http://front.auth.local/reset/123/abc/'
            mock_super_send.assert_called_once_with(
                'account/email/password_reset_key',
                'user@example.com',
                context
            )

    def test_send_mail_ignores_other_templates(self):
        """Verifica que otras plantillas de correo no sean alteradas en el envío."""
        adapter = CustomAccountAdapter()
        context = {
            'password_reset_url': 'http://api.auth.local/reset/123/abc/'
        }
        
        with patch('allauth.account.adapter.DefaultAccountAdapter.send_mail') as mock_super_send:
            adapter.send_mail(
                template_prefix='account/email/welcome',
                email='user@example.com',
                context=context
            )
            # No debe cambiar
            assert context['password_reset_url'] == 'http://api.auth.local/reset/123/abc/'
            mock_super_send.assert_called_once()

    def test_password_reset_redirect_route(self):
        """Verifica la redirección física (302) del endpoint de confirmación de password hacia el frontend."""
        client = APIClient()
        response = client.get('/password-reset/confirm/uid123/tokenabc/')
        assert response.status_code == 302
        assert response['Location'] == 'http://localhost:5173/password-reset-confirm/uid123/tokenabc/'
