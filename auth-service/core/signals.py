import logging
from django.dispatch import receiver
from allauth.account.signals import user_signed_up, email_confirmed
from .models import LegalAuditLog

logger = logging.getLogger(__name__)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@receiver(user_signed_up)
def capture_registration_audit(request, user, **kwargs):
    ip_address = get_client_ip(request)
    
    # Extraer terms_version desde request.data o request.POST
    terms_version = "UNKNOWN"
    if hasattr(request, 'data'):
        terms_version = request.data.get('terms_version', 'UNKNOWN')
    elif request.POST:
        terms_version = request.POST.get('terms_version', 'UNKNOWN')

    # Crear el registro de auditoría legal
    LegalAuditLog.objects.create(
        user=user,
        ip_address=ip_address,
        accepted_terms_version=terms_version
    )
    logger.info(f"Audit log created for user {user.username} with IP {ip_address}")

@receiver(email_confirmed)
def capture_verified_email(request, email_address, **kwargs):
    # email_address is an instance of allauth.account.models.EmailAddress
    user = email_address.user
    try:
        audit_log = LegalAuditLog.objects.get(user=user)
        audit_log.verified_email = email_address.email
        audit_log.save()
        logger.info(f"Audit log updated with verified email for user {user.username}")
    except LegalAuditLog.DoesNotExist:
        logger.warning(f"No audit log found for user {user.username} upon email confirmation")
