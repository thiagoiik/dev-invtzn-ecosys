from django.contrib import admin
from .models import Order, PaymentTransaction, CashSession, Commission, Invoice

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'store', 'total_amount', 'status', 'origin', 'created_at')
    list_filter = ('status', 'origin', 'store', 'created_at')
    search_fields = ('id', 'user', 'store__name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('order', 'provider', 'success', 'stripe_checkout_id', 'timestamp')
    list_filter = ('provider', 'success', 'timestamp')
    search_fields = ('order__id', 'stripe_checkout_id', 'stripe_payment_intent_id')

@admin.register(CashSession)
class CashSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'store', 'user', 'opening_balance', 'is_open', 'opened_at')
    list_filter = ('is_open', 'store', 'opened_at')

@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    list_display = ('order', 'vendor_id', 'amount', 'percentage', 'is_paid', 'created_at')
    list_filter = ('is_paid', 'created_at')

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'rfc', 'razon_social', 'uuid', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('order__id', 'rfc', 'razon_social', 'uuid')
