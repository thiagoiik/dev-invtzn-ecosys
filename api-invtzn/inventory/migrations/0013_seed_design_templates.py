from django.db import migrations

def seed_design_templates(apps, schema_editor):
    DesignTemplate = apps.get_model('inventory', 'DesignTemplate')
    
    # 1. XV-Onda
    DesignTemplate.objects.update_or_create(
        slug='49eeeb22',
        defaults={
            'name': 'XV-Onda',
            'tier_required': 'STANDARD',
            'vue_component_name': 'XVOnda',
            'thumbnail_url': '/preview_xv_onda.png',
            'is_active': True
        }
    )

    # 2. Boda-Amalgam
    DesignTemplate.objects.update_or_create(
        slug='dfce56a7',
        defaults={
            'name': 'Boda-Amalgam',
            'tier_required': 'PREMIUM',
            'vue_component_name': 'BodaAmalgam',
            'thumbnail_url': '/preview_boda_amalgam.png',
            'is_active': True
        }
    )

    # 3. Básica Gratis
    DesignTemplate.objects.update_or_create(
        slug='demo-basic-template',
        defaults={
            'name': 'Invitación Básica (Gratis)',
            'tier_required': 'BASIC',
            'vue_component_name': 'BasicGratis',
            'thumbnail_url': '/preview_basic_free.png',
            'is_active': True
        }
    )

def rollback_design_templates(apps, schema_editor):
    DesignTemplate = apps.get_model('inventory', 'DesignTemplate')
    DesignTemplate.objects.filter(slug__in=['49eeeb22', 'dfce56a7', 'demo-basic-template']).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('inventory', '0012_product_created_by_product_store'),
    ]

    operations = [
        migrations.RunPython(seed_design_templates, rollback_design_templates),
    ]
