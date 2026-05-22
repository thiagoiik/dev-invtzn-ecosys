import logging
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Order

logger = logging.getLogger(__name__)

@shared_task
def send_receipt_email_task(order_id):
    logger.info(f"Iniciando tarea de envío de recibo por correo para la orden #{order_id}")
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        logger.error(f"La orden #{order_id} no existe. Cancelando envío de correo.")
        return False

    # Si no hay email del cliente, no podemos enviar nada
    if not order.customer_email:
        logger.warning(f"La orden #{order_id} no tiene un customer_email definido. No se puede enviar el recibo.")
        return False

    # Datos de pago
    payment_method = "No especificado"
    try:
        if hasattr(order, 'payment') and order.payment:
            payment_method = order.payment.payment_method
    except Exception:
        pass

    # Tienda / Sucursal
    store_name = order.store.name if order.store else "ECOSYS Central"
    store_address = order.store.address if order.store else ""

    # Desglose de items
    items_list = []
    for item in order.items.all():
        seriales = list(item.serial_keys.values_list('key_value', flat=True))
        items_list.append({
            'name': item.product.name,
            'quantity': item.quantity,
            'price': float(item.price_at_sale),
            'total': float(item.price_at_sale * item.quantity),
            'is_digital': not item.product.is_physical,
            'seriales': seriales
        })

    subject = f"Recibo de Compra - Orden #{order.id} - {store_name}"
    
    # Contexto para el template de correo
    context = {
        'order': order,
        'store_name': store_name,
        'store_address': store_address,
        'items': items_list,
        'payment_method': payment_method,
        'subtotal': float(order.subtotal_amount),
        'discount': float(order.discount_amount),
        'tax': float(order.tax_amount),
        'total': float(order.total_amount),
    }

    # Template HTML inline para evitar dependencias de archivos de templates si no están configuradas
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Recibo de Compra</title>
        <style>
            body {{
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                background-color: #f8f9fa;
                margin: 0;
                padding: 0;
                color: #2d3748;
            }}
            .container {{
                max-width: 600px;
                margin: 40px auto;
                background: #ffffff;
                border-radius: 12px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
                overflow: hidden;
                border: 1px solid #e2e8f0;
            }}
            .header {{
                background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
                padding: 30px;
                text-align: center;
                color: #ffffff;
            }}
            .header h1 {{
                margin: 0;
                font-size: 24px;
                font-weight: 700;
                letter-spacing: -0.5px;
            }}
            .header p {{
                margin: 5px 0 0;
                font-size: 14px;
                opacity: 0.9;
            }}
            .content {{
                padding: 30px;
            }}
            .order-meta {{
                margin-bottom: 25px;
                padding-bottom: 20px;
                border-bottom: 1px solid #edf2f7;
            }}
            .order-meta table {{
                width: 100%;
            }}
            .order-meta td {{
                font-size: 14px;
                padding: 4px 0;
            }}
            .order-meta td.label {{
                color: #718096;
                font-weight: 500;
            }}
            .order-meta td.value {{
                text-align: right;
                font-weight: 600;
            }}
            .table-items {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 25px;
            }}
            .table-items th {{
                text-align: left;
                padding: 10px 0;
                border-bottom: 2px solid #edf2f7;
                font-size: 12px;
                text-transform: uppercase;
                color: #a0aec0;
                letter-spacing: 0.5px;
            }}
            .table-items td {{
                padding: 15px 0;
                border-bottom: 1px solid #edf2f7;
                font-size: 14px;
            }}
            .item-name {{
                font-weight: 600;
                color: #1a202c;
            }}
            .item-desc {{
                font-size: 12px;
                color: #718096;
                margin-top: 4px;
            }}
            .serial-tag {{
                display: inline-block;
                background-color: #f3f4f6;
                color: #1f2937;
                font-family: monospace;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
                margin: 2px 0;
                border: 1px solid #e5e7eb;
            }}
            .totals {{
                width: 50%;
                margin-left: auto;
                margin-bottom: 30px;
            }}
            .totals table {{
                width: 100%;
            }}
            .totals td {{
                padding: 6px 0;
                font-size: 14px;
            }}
            .totals td.label {{
                color: #718096;
            }}
            .totals td.value {{
                text-align: right;
                font-weight: 600;
            }}
            .totals tr.grand-total td {{
                border-top: 2px solid #edf2f7;
                padding-top: 12px;
                font-size: 18px;
                font-weight: 700;
                color: #4f46e5;
            }}
            .footer {{
                background-color: #f7fafc;
                padding: 20px;
                text-align: center;
                font-size: 12px;
                color: #a0aec0;
                border-top: 1px solid #edf2f7;
            }}
            .footer p {{
                margin: 5px 0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>ECOSYS</h1>
                <p>¡Gracias por tu compra en {store_name}!</p>
            </div>
            <div class="content">
                <div class="order-meta">
                    <table>
                        <tr>
                            <td class="label">Folio de Orden:</td>
                            <td class="value">#{order.id}</td>
                        </tr>
                        <tr>
                            <td class="label">Fecha:</td>
                            <td class="value">{order.created_at.strftime('%d/%m/%Y %H:%M') if order.created_at else ''}</td>
                        </tr>
                        <tr>
                            <td class="label">Método de Pago:</td>
                            <td class="value">{payment_method}</td>
                        </tr>
                    </table>
                </div>

                <table class="table-items">
                    <thead>
                        <tr>
                            <th>Concepto</th>
                            <th style="text-align: center;">Cant.</th>
                            <th style="text-align: right;">Unitario</th>
                            <th style="text-align: right;">Total</th>
                        </tr>
                    </thead>
                    <tbody>
    """

    for item in items_list:
        seriales_html = ""
        if item['is_digital'] and item['seriales']:
            seriales_html += '<div class="item-desc">Claves de activación:<br>'
            for ser in item['seriales']:
                seriales_html += f'<span class="serial-tag">{ser}</span><br>'
            seriales_html += '</div>'
            
        html_content += f"""
                        <tr>
                            <td>
                                <div class="item-name">{item['name']}</div>
                                {seriales_html}
                            </td>
                            <td style="text-align: center;">{item['quantity']}</td>
                            <td style="text-align: right;">${item['price']:.2f}</td>
                            <td style="text-align: right;">${item['total']:.2f}</td>
                        </tr>
        """

    html_content += f"""
                    </tbody>
                </table>

                <div class="totals">
                    <table>
                        <tr>
                            <td class="label">Subtotal:</td>
                            <td class="value">${context['subtotal']:.2f}</td>
                        </tr>
                        <tr>
                            <td class="label">Descuento:</td>
                            <td class="value">-${context['discount']:.2f}</td>
                        </tr>
                        <tr>
                            <td class="label">Impuestos:</td>
                            <td class="value">${context['tax']:.2f}</td>
                        </tr>
                        <tr class="grand-total">
                            <td class="label">Total:</td>
                            <td class="value">${context['total']:.2f}</td>
                        </tr>
                    </table>
                </div>
            </div>
            <div class="footer">
                <p>{store_name}</p>
                <p>{store_address}</p>
                <p>Este correo es un recibo electrónico de tu transacción.</p>
                <p>&copy; {order.created_at.year if order.created_at else 2026} ECOSYS. Todos los derechos reservados.</p>
            </div>
        </div>
    </body>
    </html>
    """

    text_content = f"""
    ECOSYS - ¡Gracias por tu compra!
    
    Folio de Orden: #{order.id}
    Fecha: {order.created_at.strftime('%d/%m/%Y %H:%M') if order.created_at else ''}
    Método de Pago: {payment_method}
    Sucursal: {store_name}
    
    Detalle de Compra:
    """
    for item in items_list:
        text_content += f"\n- {item['quantity']}x {item['name']} - ${item['price']:.2f} (Total: ${item['total']:.2f})"
        if item['is_digital'] and item['seriales']:
            text_content += "\n  Claves de activación:\n"
            for ser in item['seriales']:
                text_content += f"  - {ser}\n"
                
    text_content += f"""
    
    Subtotal: ${context['subtotal']:.2f}
    Descuento: -${context['discount']:.2f}
    Impuestos: ${context['tax']:.2f}
    Total: ${context['total']:.2f}
    
    {store_name}
    {store_address}
    
    Este correo es un recibo electrónico de tu transacción.
    """

    try:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=None,  # Usa DEFAULT_FROM_EMAIL
            to=[order.customer_email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        logger.info(f"Recibo enviado con éxito al correo {order.customer_email} para la orden #{order.id}")
        return True
    except Exception as e:
        logger.error(f"Error enviando correo de recibo para la orden #{order.id}: {str(e)}")
        return False
