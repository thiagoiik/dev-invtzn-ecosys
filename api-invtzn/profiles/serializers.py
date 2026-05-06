from rest_framework import serializers
from django.db.models import Sum
from .models import UserProfile, WalletLog, CommunicationLog

class WalletLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletLog
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    # Campo dinámico para el saldo actual
    current_balance = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'remote_auth_id', 
            'custom_role', 
            'phone_number', 
            'customer_type', 
            'base_commission_rate', 
            'current_balance', # Campo calculado
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

    def get_current_balance(self, obj):
        """
        Suma todos los 'amount' de los WalletLogs asociados a este usuario.
        """
        # Accedemos a través del related_name 'wallet_logs' definido en el modelo
        total = obj.wallet_logs.aggregate(total=Sum('amount'))['total']
        return total if total is not None else 0.00