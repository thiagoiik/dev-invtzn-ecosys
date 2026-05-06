from django.db import models
from profiles.models import UserProfile

class EventContext(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=200, help_text="Ej: Boda de Martha y Pekas")
    event_type = models.CharField(max_length=50, default="BODA")
    main_date = models.DateField()
    location_name = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.main_date}"