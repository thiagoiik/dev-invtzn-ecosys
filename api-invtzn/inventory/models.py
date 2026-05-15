from django.db import models

class Store(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
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

    def __str__(self):
        return f"{self.name} (${self.base_price})"

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