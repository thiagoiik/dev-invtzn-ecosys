from django.db import migrations

def seed_upgrade_products(apps, schema_editor):
    Product = apps.get_model('inventory', 'Product')
    # Create Standard Upgrade
    Product.objects.get_or_create(
        sku='UPGRADE-STD',
        defaults={
            'name': 'Pase de Edición Standard',
            'description': 'Desbloquea música de fondo, cuenta regresiva y personalización de temas.',
            'product_type': 'DIGITAL',
            'base_price': 149.00,
            'has_template': False,
            'tier_level': 'STANDARD',
            'is_active': True
        }
    )
    # Create Premium Upgrade
    Product.objects.get_or_create(
        sku='UPGRADE-PREM',
        defaults={
            'name': 'Pase de Edición Premium',
            'description': 'Desbloquea itinerario, sobres 3D, música de fondo personalizada y metadatos Open Graph.',
            'product_type': 'DIGITAL',
            'base_price': 299.00,
            'has_template': False,
            'tier_level': 'PREMIUM',
            'is_active': True
        }
    )

def rollback_upgrade_products(apps, schema_editor):
    Product = apps.get_model('inventory', 'Product')
    Product.objects.filter(sku__in=['UPGRADE-STD', 'UPGRADE-PREM']).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('inventory', '0007_designtemplate_product_features_product_tier_level_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_upgrade_products, rollback_upgrade_products),
    ]
