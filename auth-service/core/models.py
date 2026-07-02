from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class LegalAuditLog(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="audit_log")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    verified_email = models.EmailField(null=True, blank=True)
    accepted_terms_version = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Audit for {self.user.username} (Terms: {self.accepted_terms_version})"
