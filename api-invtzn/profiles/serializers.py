from rest_framework import serializers
from django.db.models import Sum
from .models import UserProfile, WalletLog, CommunicationLog, SiteReview

class WalletLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletLog
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'remote_auth_id', 
            'full_name',
            'email',
            'custom_role', 
            'phone_number', 
            'customer_type', 
            'base_commission_rate', 
            'current_balance',
            'internal_notes', 
            'assigned_store',
            'vendor_mode',
            'created_at', 
            'updated_at'
        ]
        # Protegemos campos críticos de edición desde el Frontend
        read_only_fields = [
            'remote_auth_id', 
            'custom_role', 
            'base_commission_rate', 
            'current_balance'
        ]

class SiteReviewSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = SiteReview
        fields = [
            'id',
            'user',
            'user_email',
            'reviewer_name',
            'rating',
            'comment',
            'is_approved',
            'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']


class CommunicationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunicationLog
        fields = ['id', 'user', 'channel', 'subject', 'sent_at']