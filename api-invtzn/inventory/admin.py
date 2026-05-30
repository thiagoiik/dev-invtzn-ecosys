from django.contrib import admin
from .models import Product, DesignTemplate, Store, ProductSerialKey

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'stripe_account_id', 'stripe_onboarding_completed', 'is_active')
    list_filter = ('is_active', 'stripe_onboarding_completed', 'city')
    search_fields = ('name', 'city', 'stripe_account_id')
    fieldsets = (
        ('Información General', {
            'fields': ('name', 'address', 'city', 'is_active')
        }),
        ('Stripe Connect', {
            'fields': ('stripe_account_id', 'stripe_onboarding_completed')
        }),
    )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Columnas visibles en la lista
    list_display = ('name', 'product_type', 'tier_level', 'base_price', 'is_active', 'is_physical', 'stock_quantity', 'has_template', 'created_by', 'store')
    # Filtros laterales
    list_filter = ('product_type', 'tier_level', 'is_active', 'is_physical', 'has_template', 'store')
    # Buscador
    search_fields = ('name', 'description')
    # Organizar el formulario de edición
    fieldsets = (
        ('Información General', {
            'fields': ('name', 'description', 'product_type', 'tier_level', 'base_price', 'is_active')
        }),
        ('Control de Stock e Inventario', {
            'fields': ('is_physical', 'stock_quantity')
        }),
        ('Configuración Digital', {
            'fields': ('has_template', 'features')
        }),
        ('Información de Origen', {
            'fields': ('created_by', 'store')
        }),
    )


@admin.register(DesignTemplate)
class DesignTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'tier_required', 'vue_component_name', 'is_active', 'is_featured_on_landing')
    list_filter = ('tier_required', 'is_active', 'is_featured_on_landing')
    search_fields = ('name', 'slug', 'vue_component_name')

@admin.register(ProductSerialKey)
class ProductSerialKeyAdmin(admin.ModelAdmin):
    list_display = ('product', 'key_value', 'is_assigned', 'assigned_at', 'created_at')
    list_filter = ('is_assigned', 'product')
    search_fields = ('key_value', 'product__name')