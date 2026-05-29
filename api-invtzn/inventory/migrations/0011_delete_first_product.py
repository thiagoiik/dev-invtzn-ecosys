from django.db import migrations

def delete_first_product(apps, schema_editor):
    Product = apps.get_model('inventory', 'Product')
    Deployment = apps.get_model('deployments', 'Deployment')
    Order = apps.get_model('sales', 'Order')
    OrderItem = apps.get_model('sales', 'OrderItem')
    
    # 1. Eliminar órdenes que contengan el producto 1 (limpieza de cascada)
    order_items = OrderItem.objects.filter(product_id=1)
    for item in order_items:
        Order.objects.filter(id=item.order_id).delete()
        
    # 2. Eliminar invitaciones/sandbox vinculadas al producto 1 y sus órdenes residuales
    deployments = Deployment.objects.filter(product_id=1)
    for dep in deployments:
        Order.objects.filter(deployment_id=dep.id).delete()
        dep.delete()

    # 3. Eliminar el primer producto definitivamente
    Product.objects.filter(id=1).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_product_template_slug'),
        ('deployments', '0009_systemlog_deployment_creation_mode'),
        ('sales', '0012_order_coupon'),
    ]

    operations = [
        migrations.RunPython(delete_first_product),
    ]
