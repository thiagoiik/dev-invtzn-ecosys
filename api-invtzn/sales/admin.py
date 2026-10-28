from django.contrib import admin
from .models import Order, PaymentTransaction, CashSession, Commission, Invoice, OrderItem, ShippingAddress

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class ShippingAddressInline(admin.StackedInline):
    model = ShippingAddress
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'store', 'total_amount', 'status', 'fulfillment_status', 'origin', 'created_at')
    list_filter = ('status', 'fulfillment_status', 'origin', 'store', 'created_at')
    search_fields = ('id', 'user', 'store__name', 'shipping_address__recipient_name', 'shipping_address__city')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [OrderItemInline, ShippingAddressInline]

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

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'recipient_name', 'city', 'state', 'phone')
    search_fields = ('order__id', 'recipient_name', 'city', 'state', 'phone')

from .models import Coupon, DirectDiscount

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percentage', 'discount_fixed', 'active', 'current_uses', 'max_uses', 'valid_from', 'valid_to')
    list_filter = ('active', 'valid_from', 'valid_to')
    search_fields = ('code',)

@admin.register(DirectDiscount)
class DirectDiscountAdmin(admin.ModelAdmin):
    list_display = ('order', 'authorized_by', 'amount')
    search_fields = ('order__id', 'authorized_by')
