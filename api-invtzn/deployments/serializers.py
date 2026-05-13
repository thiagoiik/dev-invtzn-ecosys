from rest_framework import serializers
from .models import Deployment

class DeploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deployment
        fields = '__all__'
        read_only_fields = ('user', 'status', 'created_at', 'updated_at')
