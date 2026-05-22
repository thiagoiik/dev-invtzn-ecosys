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

    class TierLevel(models.TextChoices):
        BASIC = 'BASIC', 'Básico / Gratis'
        STANDARD = 'STANDARD', 'Standard'
        PREMIUM = 'PREMIUM', 'Premium'

    tier_level = models.CharField(
        max_length=20, 
        choices=TierLevel.choices, 
        default=TierLevel.BASIC,
        help_text="Nivel comercial de suscripción o tier del producto"
    )
    features = models.JSONField(
        default=dict, 
        blank=True, 
        help_text="Configuración de bloques y flags permitidos"
    )

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

class DesignTemplate(models.Model):
    """
    Define un diseño visual/estética independiente que puede ser utilizado por
    las invitaciones según el nivel de tier contratado.
    """
    class TierRequired(models.TextChoices):
        BASIC = 'BASIC', 'Básico / Gratis'
        STANDARD = 'STANDARD', 'Standard'
        PREMIUM = 'PREMIUM', 'Premium'

    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=100, unique=True, help_text="Slug único de identificación para la URL")
    
    tier_required = models.CharField(
        max_length=20, 
        choices=TierRequired.choices, 
        default=TierRequired.BASIC,
        help_text="Tier mínimo requerido para poder usar este diseño"
    )
    
    vue_component_name = models.CharField(
        max_length=100, 
        help_text="Nombre del componente layout en el Frontend (ej: 'ClassicGold')"
    )
    
    default_config = models.JSONField(
        default=dict, 
        blank=True,
        help_text="Configuración inicial del diseño: colores, fuentes, etc."
    )
    
    thumbnail_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Miniatura visual para el catálogo de selección"
    )
    
    demo_slug = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Slug de una invitación demo real para ver este diseño en vivo"
    )
    
    is_active = models.BooleanField(default=True)
    is_featured_on_landing = models.BooleanField(default=False, help_text="Destacar este diseño en la landing page")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (Requiere {self.tier_required})"

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