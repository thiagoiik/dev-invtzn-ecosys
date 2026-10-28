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

@pytest.mark.django_db
def test_public_reviews_allow_any():
    # 1. Setup
    from profiles.models import SiteReview
    client = APIClient()
    
    user = UserProfile.objects.create(remote_auth_id=10, custom_role='CLIENT')
    SiteReview.objects.create(user=user, reviewer_name="María", comment="Excelente", rating=5, is_approved=True)
    SiteReview.objects.create(user=user, reviewer_name="Juan", comment="Malo", rating=2, is_approved=False)
    
    # 2. Acción (petición anónima a reviews/public)
    response = client.get('/api/v1/reviews/public/')
    
    # 3. Verificación
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['reviewer_name'] == "María"

@pytest.mark.django_db
def test_reviews_require_auth():
    client = APIClient()
    response = client.get('/api/v1/reviews/')
    assert response.status_code == 403

@pytest.mark.django_db
def test_toggle_review_approval_requires_staff_role():
    from profiles.models import SiteReview
    client = APIClient()
    
    client_user = UserProfile.objects.create(remote_auth_id=1, custom_role='CLIENT')
    admin_user = UserProfile.objects.create(remote_auth_id=2, custom_role='ADMIN')
    review = SiteReview.objects.create(user=client_user, reviewer_name="Test", comment="Ok", rating=4, is_approved=False)
    
    # 1. Intento sin autenticar
    response = client.post(f'/api/v1/reviews/{review.id}/toggle-approve/')
    assert response.status_code == 403
    
    # 2. Intento con rol CLIENT
    client.force_authenticate(user=client_user)
    response = client.post(f'/api/v1/reviews/{review.id}/toggle-approve/')
    assert response.status_code == 403
    
    # 3. Intento con rol ADMIN
    client.force_authenticate(user=admin_user)
    response = client.post(f'/api/v1/reviews/{review.id}/toggle-approve/')
    assert response.status_code == 200
    assert response.data['is_approved'] is True
    
    review.refresh_from_db()
    assert review.is_approved is True

@pytest.mark.django_db
def test_create_review_authenticated():
    from profiles.models import SiteReview
    client = APIClient()
    user = UserProfile.objects.create(remote_auth_id=15, custom_role='CLIENT')
    client.force_authenticate(user=user)
    
    payload = {
        'reviewer_name': 'Test User',
        'rating': 4,
        'comment': 'Me encanto el servicio, muy facil de usar.'
    }
    
    response = client.post('/api/v1/reviews/', payload)
    assert response.status_code == 201
    assert response.data['reviewer_name'] == 'Test User'
    assert response.data['rating'] == 4
    assert response.data['comment'] == 'Me encanto el servicio, muy facil de usar.'
    assert response.data['is_approved'] is False  # Por defecto no aprobado
    
    # Verificar en BD
    review = SiteReview.objects.get(id=response.data['id'])
    assert review.user == user


@pytest.mark.django_db
def test_notifications_list_and_self_cleaning_for_admin():
    client = APIClient()
    
    # 1. Setup Admin user
    admin_user = UserProfile.objects.create(remote_auth_id=100, custom_role='ADMIN')
    client.force_authenticate(user=admin_user)
    
    # 2. Setup Deployments (one DRAFT, one ACTIVE)
    from deployments.models import Deployment
    from inventory.models import Product
    product = Product.objects.create(name='Test Product', base_price=10.00, product_type='DIGITAL')
    
    draft_dep = Deployment.objects.create(user=99, product=product, status=Deployment.StatusChoices.DRAFT)
    active_dep = Deployment.objects.create(user=99, product=product, status=Deployment.StatusChoices.ACTIVE)
    
    # 3. Create CommunicationLog notifications
    from profiles.models import CommunicationLog
    
    # Notif 1 for draft_dep (should be shown)
    CommunicationLog.objects.create(
        user=admin_user,
        channel=CommunicationLog.Channel.SYSTEM,
        subject=f"El Diseñador Leopardo solicita revisión (ID: {draft_dep.id})"
    )
    
    # Notif 2 for active_dep (should NOT be shown - self-cleaning)
    CommunicationLog.objects.create(
        user=admin_user,
        channel=CommunicationLog.Channel.SYSTEM,
        subject=f"El Diseñador Mamba solicita revisión (ID: {active_dep.id})"
    )
    
    # Notif 3 without ID in subject (should be shown)
    CommunicationLog.objects.create(
        user=admin_user,
        channel=CommunicationLog.Channel.SYSTEM,
        subject="Notificación del sistema sin ID de invitación"
    )
    
    # 4. Request notifications endpoint
    response = client.get('/api/v1/profiles/notifications/')
    assert response.status_code == 200
    assert len(response.data) == 2
    
    subjects = [n['subject'] for n in response.data]
    # Verify the DRAFT one and the one without ID are returned
    assert f"El Diseñador Leopardo solicita revisión (ID: {draft_dep.id})" in subjects
    assert "Notificación del sistema sin ID de invitación" in subjects
    # Verify the ACTIVE template one is filtered out (self-cleaned)
    assert f"El Diseñador Mamba solicita revisión (ID: {active_dep.id})" not in subjects
