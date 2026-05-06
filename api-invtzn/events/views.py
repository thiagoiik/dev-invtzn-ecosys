from rest_framework import viewsets
from .models import EventContext
from .serializers import EventContextSerializer

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventContextSerializer

    def get_queryset(self):
        # request.user.id es el 8 que ya validamos
        return EventContext.objects.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)