from django.db import models

class Store(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    # Stripe Connect integration
    stripe_account_id = models.CharField(max_length=100, blank=True, null=True, help_text="ID de la cuenta de Stripe Connect")
    stripe_onboarding_completed = models.BooleanField(default=False)
    
    # Propiedad y Franquicia
    owner = models.ForeignKey('profiles.UserProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='owned_stores', help_text="Dueño / Franquiciatario de esta sucursal")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.city})"

class Product(models.Model):
    class ProductType(models.TextChoices):
        DIGITAL = 'DIGITAL', 'Invitación Digital'
        PHYSICAL = 'PHYSICAL', 'Producto Físico (Impresos)'
        SERVICE = 'SERVICE', 'Servicio / Boutique'

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    product_type = models.CharField(
        max_length=20, 
        choices=ProductType.choices, 
        default=ProductType.DIGITAL
    )
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    
    # Control de Stock
    is_physical = models.BooleanField(default=False)
    stock_quantity = models.IntegerField(default=0)
    
    # ¿Este producto genera un despliegue automático?
    has_template = models.BooleanField(default=False)

    # NUEVOS CAMPOS ETAPA 2
    sku = models.CharField(max_length=50, unique=True, null=True, blank=True, help_text="Código único de inventario")
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Precio de costo")
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.16, help_text="Porcentaje de impuesto ej. 0.16")
    min_stock = models.IntegerField(default=0, help_text="Stock mínimo para alertas")

    def __str__(self):
        return f"{self.name} (${self.base_price})"

class StoreStock(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='stocks')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='store_stocks')
    quantity = models.IntegerField(default=0)

    class Meta:
        unique_together = ('store', 'product')

    def __str__(self):
        return f"Stock de {self.product.name} en {self.store.name}: {self.quantity}"

class Template(models.Model):
    """
    Define el 'diseño' base que se usará en Vue.
    Ejemplo: 'Template Boda Clásica' -> apunta al componente Vue 'BodaOro.vue'
    """
    product = models.OneToOneField(
        Product, 
        on_delete=models.CASCADE, 
        related_name='template_config'
    )
    vue_component_name = models.CharField(
        max_length=100, 
        help_text="Nombre del componente en el Front (ej: 'ClassicGold')"
    )
    default_config = models.JSONField(
        default=dict, 
        help_text="Configuración inicial: colores, fuentes, etc."
    )

    def __str__(self):
        return f"Configuración para {self.product.name}"

class ProductSerialKey(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='serial_keys')
    key_value = models.CharField(max_length=255, unique=True)
    is_assigned = models.BooleanField(default=False)
    order_item = models.ForeignKey(
        'sales.OrderItem', 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name='serial_keys'
    )
    assigned_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.key_value} (Asignada: {self.is_assigned})"