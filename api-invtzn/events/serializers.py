from rest_framework import serializers
from .models import EventContext

class EventContextSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventContext
        fields = '__all__'
        read_only_fields = ['user']