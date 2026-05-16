from django.contrib import admin

from .models import BankSyncLog

@admin.register(BankSyncLog)
class BankSyncLogAdmin(admin.ModelAdmin):
    list_display = ('external_id', 'amount', 'sender_name', 'is_reconciled', 'timestamp')
    list_filter = ('is_reconciled', 'sender_bank', 'timestamp')
    search_fields = ('external_id', 'sender_name', 'description')
