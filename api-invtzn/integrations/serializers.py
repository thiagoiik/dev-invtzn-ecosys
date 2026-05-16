from rest_framework import serializers
from .models import BankSyncLog

class BankSyncLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankSyncLog
        fields = '__all__'
