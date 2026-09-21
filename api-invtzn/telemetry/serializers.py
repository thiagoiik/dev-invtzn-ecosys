from rest_framework import serializers
from .models import SessionRecording

from profiles.models import UserProfile

class SessionRecordingListSerializer(serializers.ModelSerializer):
    """
    Serializer para listar grabaciones omitiendo el payload gigante.
    """
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = SessionRecording
        fields = ['id', 'user_id', 'user_name', 'role', 'environment', 'user_agent', 'window_width', 'window_height', 'created_at']

    def get_user_name(self, obj):
        if obj.user_id:
            try:
                user = UserProfile.objects.get(pk=obj.user_id)
                return user.full_name or f"Usuario {obj.user_id}"
            except UserProfile.DoesNotExist:
                return f"Desconocido ({obj.user_id})"
        return "Anónimo"

class SessionRecordingDetailSerializer(serializers.ModelSerializer):
    """
    Serializer completo, incluye el payload JSON para reproducir el video.
    """
    class Meta:
        model = SessionRecording
        fields = '__all__'
