from django.contrib import admin
from .models import UserProfile, WalletLog, CommunicationLog

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('remote_auth_id', 'custom_role', 'customer_type', 'current_balance', 'created_at')
    list_filter = ('custom_role', 'customer_type')
    search_fields = ('remote_auth_id', 'phone_number')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(WalletLog)
class WalletLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'reason', 'timestamp')
    list_filter = ('reason',)
    search_fields = ('user__remote_auth_id',)

@admin.register(CommunicationLog)
class CommunicationLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'channel', 'subject', 'sent_at')
    list_filter = ('channel',)
    search_fields = ('user__remote_auth_id', 'subject')