import pytest
from rest_framework.test import APIClient
from decimal import Decimal
from profiles.models import UserProfile, WalletLog

@pytest.mark.django_db
def test_wallet_log_updates_current_balance():
    # 1. Preparación (Setup)
    user = UserProfile.objects.create(remote_auth_id=1, custom_role='CLIENT')
    
    # Verificamos el saldo inicial
    assert user.current_balance == Decimal('0.00')

    # 2. Acción: Creamos un registro en la billetera
    WalletLog.objects.create(
        user=user, 
        amount=Decimal('500.00'), 
        reason='BANK_DEPOSIT'
    )
    
    # Refrescamos el usuario de la DB
    user.refresh_from_db()

    # 3. Verificación (Assert)
    assert user.current_balance == Decimal('500.00')

@pytest.mark.django_db
def test_get_my_profile():
    # 1. Setup
    client = APIClient()
    
    # Simulamos que tenemos un usuario autenticado
    # DRF Testing Client nos permite simular requests forzando la autenticación
    user = UserProfile.objects.create(remote_auth_id=99, custom_role='CLIENT')
    client.force_authenticate(user=user)
    
    # 2. Acción
    response = client.get('/api/v1/profiles/me/')
    
    # 3. Verificación
    assert response.status_code == 200
    assert response.data['remote_auth_id'] == 99
