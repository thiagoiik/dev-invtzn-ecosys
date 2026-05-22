from django.contrib import admin
from .models import Product, Template, Store, ProductSerialKey

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
    list_display = ('name', 'product_type', 'base_price', 'is_active', 'is_physical', 'stock_quantity', 'has_template')
    # Filtros laterales
    list_filter = ('product_type', 'is_active', 'is_physical', 'has_template')
    # Buscador
    search_fields = ('name', 'description')
    # Organizar el formulario de edición
    fieldsets = (
        ('Información General', {
            'fields': ('name', 'description', 'product_type', 'base_price', 'is_active')
        }),
        ('Control de Stock e Inventario', {
            'fields': ('is_physical', 'stock_quantity')
        }),
        ('Configuración Digital', {
            'fields': ('has_template',)
        }),
    )

@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('product', 'vue_component_name')
    search_fields = ('product__name', 'vue_component_name')
    # Ayuda a que el JSON se vea mejor en el admin (opcional)
    # Si quieres que se vea como código, puedes usar librerías extra, 
    # pero por defecto Django ya muestra el campo de texto JSON.

@admin.register(ProductSerialKey)
class ProductSerialKeyAdmin(admin.ModelAdmin):
    list_display = ('product', 'key_value', 'is_assigned', 'assigned_at', 'created_at')
    list_filter = ('is_assigned', 'product')
    search_fields = ('key_value', 'product__name')