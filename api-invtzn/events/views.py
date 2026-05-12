from rest_framework import viewsets
from .models import EventContext
from .serializers import EventContextSerializer

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventContextSerializer

    def get_queryset(self):
        # Aseguramos que el cliente solo vea y edite sus eventos
        return EventContext.objects.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)