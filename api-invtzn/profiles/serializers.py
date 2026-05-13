from rest_framework import serializers
from django.db.models import Sum
from .models import UserProfile, WalletLog, CommunicationLog

class WalletLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletLog
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'remote_auth_id', 
            'custom_role', 
            'phone_number', 
            'customer_type', 
            'base_commission_rate', 
            'current_balance',
            'internal_notes', 
            'created_at', 
            'updated_at'
        ]
        # Protegemos campos críticos de edición desde el Frontend
        read_only_fields = [
            'remote_auth_id', 
            'custom_role', 
            'base_commission_rate', 
            'current_balance', 
            'internal_notes'
        ]