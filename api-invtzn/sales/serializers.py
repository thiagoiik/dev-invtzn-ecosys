from rest_framework import serializers
from .models import Order, CashSession, Commission

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(required=False)
    
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('status', 'created_at', 'updated_at')

class CashSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashSession
        fields = '__all__'
        read_only_fields = ('opened_at', 'is_open')

class CommissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commission
        fields = '__all__'
