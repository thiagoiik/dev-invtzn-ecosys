from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, CashSession, Commission
from .serializers import OrderSerializer, CashSessionSerializer, CommissionSerializer
from profiles.models import UserProfile
from django.db import models

from rest_framework.decorators import action
from integrations.stripe_provider import StripeProvider

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], url_path='pay-stripe')
    def pay_with_stripe(self, request, pk=None):
        order = self.get_object()
        success_url = request.data.get('success_url', 'http://localhost:5173/checkout/success')
        cancel_url = request.data.get('cancel_url', 'http://localhost:5173/checkout/cancel')
        
        try:
            url = StripeProvider.create_checkout_session(order, success_url, cancel_url)
            return Response({'url': url})
        except Exception as e:
            return Response({'error': str(e)}, status=400)

    @action(detail=False, methods=['post'], url_path='validate-coupon')
    def validate_coupon(self, request):
        from .models import Coupon
        code = request.data.get('code', '').strip()
        if not code:
            return Response({'error': 'El código del cupón es requerido.'}, status=400)
            
        try:
            coupon = Coupon.objects.get(code__iexact=code)
            if not coupon.is_valid():
                return Response({'error': 'Este cupón ha expirado, está inactivo o superó su límite de usos.'}, status=400)
                
            return Response({
                'id': coupon.id,
                'code': coupon.code,
                'discount_percentage': float(coupon.discount_percentage),
                'discount_fixed': float(coupon.discount_fixed),
                'message': 'Cupón válido aplicado'
            })
        except Coupon.DoesNotExist:
            return Response({'error': 'Cupón no encontrado o inválido.'}, status=404)

    @action(detail=True, methods=['post'], url_path='force-activation')
    def force_activation(self, request, pk=None):
        """
        DevTool: Simula la llegada de un Webhook de Stripe y fuerza el pago y activación de la orden.
        """
        profile = self._get_user_profile()
        if not profile or profile.custom_role not in ['ADMIN', 'FRANCHISEE']:
            return Response({'error': 'No autorizado'}, status=403)
            
        order = self.get_object()
        if order.status == Order.StatusChoices.COMPLETED:
            return Response({'error': 'La orden ya está completada'}, status=400)
            
        order.status = Order.StatusChoices.COMPLETED
        order.save()
        
        if order.deployment:
            from deployments.models import Deployment
            order.deployment.is_paid = True
            order.deployment.status = Deployment.StatusChoices.LIVE
            order.deployment.save()
            
        if hasattr(order, 'payment') and order.payment:
            order.payment.success = True
            order.payment.save()
            
        return Response({'success': True, 'message': 'Orden forzada a completada y despliegue activado.'})

    @action(detail=False, methods=['post'], url_path='force-activation-by-deployment')
    def force_activation_by_deployment(self, request):
        """
        DevTool: Localiza la orden de pago pendiente más reciente asociada a un ID de Diseño
        (deployment_id) y fuerza su cobro para activarla.
        """
        profile = self._get_user_profile()
        if not profile or profile.custom_role not in ['ADMIN', 'FRANCHISEE']:
            return Response({'error': 'No autorizado'}, status=403)
            
        deployment_id = request.data.get('deployment_id')
        if not deployment_id:
            return Response({'error': 'El ID del diseño (deployment_id) es requerido.'}, status=400)
            
        # Localizar la última orden creada para este diseño que no esté completada o esté pendiente
        order = Order.objects.filter(deployment_id=deployment_id).order_by('-created_at').first()
        if not order:
            return Response({'error': f'No se encontró ninguna orden de pago asociada al diseño #{deployment_id}.'}, status=404)
            
        if order.status == Order.StatusChoices.COMPLETED:
            return Response({'error': f'La orden #{order.id} asociada al diseño ya está completada.'}, status=400)
            
        # Completar la orden. El handler post_save se encargará de activar el deployment y marcarlo como pagado.
        order.status = Order.StatusChoices.COMPLETED
        order.save()
        
        # Sincronizar el estado del pago por si acaso
        if hasattr(order, 'payment') and order.payment:
            order.payment.success = True
            order.payment.save()
            
        return Response({
            'success': True,
            'message': f'Orden #{order.id} para el diseño #{deployment_id} completada con éxito.'
        })

    @action(detail=True, methods=['post'], url_path='complete-pos')
    def complete_pos_order(self, request, pk=None):
        from django.utils import timezone
        from django.db import transaction
        from django.core.exceptions import ValidationError as DjangoValidationError
        from rest_framework.exceptions import ValidationError
        from .models import PaymentTransaction, CashSession
        from inventory.models import ProductSerialKey
        from .tasks import send_receipt_email_task
        
        order = self.get_object()
        if order.status != Order.StatusChoices.PENDING:
            return Response({'error': 'Esta orden no se encuentra pendiente.'}, status=status.HTTP_400_BAD_REQUEST)
            
        profile = self._get_user_profile()
        if not profile or profile.custom_role not in [UserProfile.Role.ADMIN, UserProfile.Role.FRANCHISEE, UserProfile.Role.MANAGER, UserProfile.Role.VENDOR]:
            return Response({'error': 'No tienes permisos para completar órdenes de caja.'}, status=status.HTTP_403_FORBIDDEN)
            
        payment_method = request.data.get('payment_method')
        if payment_method not in ['CASH', 'CARD']:
            return Response({'error': 'El método de pago para POS debe ser CASH o CARD.'}, status=status.HTTP_400_BAD_REQUEST)
            
        if payment_method == 'CASH':
            # Validar que tenga una sesión de caja activa
            if not profile.assigned_store:
                return Response({'error': 'No tienes una sucursal asignada.'}, status=status.HTTP_400_BAD_REQUEST)
                
            session_exists = CashSession.objects.filter(
                user=self.request.user.id,
                store=profile.assigned_store,
                is_open=True
            ).exists()
            if not session_exists:
                return Response({'error': 'Debes abrir un turno de caja para registrar pagos en efectivo.'}, status=status.HTTP_400_BAD_REQUEST)

        customer_email = request.data.get('customer_email')

        try:
            with transaction.atomic():
                # Primero, si hay items digitales, asignamos los seriales usando select_for_update FIFO
                for item in order.items.all():
                    if not item.product.is_physical:
                        # Buscamos seriales sin asignar ordenados por id (FIFO) bloqueándolos
                        keys = list(
                            ProductSerialKey.objects.select_for_update()
                            .filter(product=item.product, is_assigned=False)
                            .order_by('id')[:item.quantity]
                        )
                        if len(keys) < item.quantity:
                            raise ValidationError({
                                "error": f"No hay suficientes claves de activación (seriales) para '{item.product.name}'. Requeridos: {item.quantity}, Disponibles: {len(keys)}."
                            })
                        
                        # Asignamos
                        for key in keys:
                            key.is_assigned = True
                            key.order_item = item
                            key.assigned_at = timezone.now()
                            key.save()

                # Guardar el correo si fue suministrado
                if customer_email:
                    order.customer_email = customer_email

                # Modificar estado de la orden
                order.status = Order.StatusChoices.COMPLETED
                
                # Si fue en POS, vincular al vendedor y tienda correspondientes si no estaban
                if not order.vendor_id:
                    order.vendor_id = request.user.id
                    order.origin = Order.OriginChoices.POS
                if not order.store and profile.assigned_store:
                    order.store = profile.assigned_store
                    
                order.save()
                
                # Registrar transacción
                PaymentTransaction.objects.update_or_create(
                    order=order,
                    defaults={
                        'provider': 'POS_TERMINAL',
                        'payment_method': payment_method,
                        'success': True,
                        'transaction_id': f"POS-{order.id}-{int(timezone.now().timestamp())}"
                    }
                )

                # Si es un item digital (o si tiene diseño asignado), disparar activación de Deployment
                # Esto ya formaba parte de las especificaciones previas
                if order.deployment:
                    order.deployment.status = 'ACTIVE'
                    order.deployment.save()

        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f"Error al procesar la asignación de seriales o guardar orden: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Disparar tarea Celery asíncrona de envío de recibo por correo
        if order.customer_email:
            try:
                send_receipt_email_task.delay(order.id)
            except Exception as e:
                # Si Celery falla al encolar, registramos el error pero no bloqueamos la respuesta exitosa del POS
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Error al encolar send_receipt_email_task para orden #{order.id}: {str(e)}")

        # Retornamos los datos actualizados incluyendo los seriales asignados
        # Serializamos usando OrderSerializer para incluir items con sus serial_keys
        serialized_order = OrderSerializer(order).data

        return Response({
            'success': True,
            'order': serialized_order,
            'message': 'Venta procesada exitosamente y recibo encolado por correo.'
        })

    def _get_user_profile(self):
        try:
            return UserProfile.objects.get(remote_auth_id=self.request.user.id)
        except UserProfile.DoesNotExist:
            return None

    def get_queryset(self):
        profile = self._get_user_profile()
        if not profile:
            return Order.objects.none()
            
        if profile.custom_role == UserProfile.Role.ADMIN:
            return Order.objects.all().order_by('-created_at')
            
        if profile.custom_role == UserProfile.Role.FRANCHISEE:
            # El franquiciatario ve órdenes de sus tiendas
            from inventory.models import Store
            owned_stores = Store.objects.filter(owner=profile)
            return Order.objects.filter(store__in=owned_stores).order_by('-created_at')

        if profile.custom_role == UserProfile.Role.MANAGER:
            # El gerente ve órdenes de su tienda
            if profile.assigned_store:
                return Order.objects.filter(store=profile.assigned_store).order_by('-created_at')
            return Order.objects.none()

        if profile.custom_role == UserProfile.Role.VENDOR:
            return Order.objects.filter(
                models.Q(user=self.request.user.id) | 
                models.Q(vendor_id=self.request.user.id)
            ).order_by('-created_at')
            
        return Order.objects.filter(user=self.request.user.id).order_by('-created_at')

    def perform_create(self, serializer):
        profile = self._get_user_profile()
        role = profile.custom_role if profile else UserProfile.Role.CLIENT
        
        # Valores por defecto
        save_kwargs = {}
        
        if role in [UserProfile.Role.ADMIN, UserProfile.Role.FRANCHISEE, UserProfile.Role.MANAGER, UserProfile.Role.VENDOR]:
            # Si el Staff registra la orden para un cliente (Buscó al cliente en el POS)
            if 'user' in self.request.data:
                save_kwargs['vendor_id'] = self.request.user.id
                save_kwargs['origin'] = Order.OriginChoices.POS
                if profile and profile.assigned_store:
                    save_kwargs['store'] = profile.assigned_store
            else:
                # El staff compra para sí mismo (B2C flow siendo staff)
                save_kwargs['user'] = self.request.user.id
                save_kwargs['origin'] = Order.OriginChoices.ONLINE
        else:
            # Cliente normal comprando online
            save_kwargs['user'] = self.request.user.id
            save_kwargs['origin'] = Order.OriginChoices.ONLINE

        # Vincular diseño si viene de un Sandbox/Draft
        deployment_id = self.request.data.get('deployment')
        if deployment_id:
            from deployments.models import Deployment
            try:
                dep = Deployment.objects.get(id=deployment_id)
                # Obtener el rol del propietario actual (si tiene)
                current_owner_role = None
                if dep.user:
                    try:
                        owner_profile = UserProfile.objects.get(remote_auth_id=dep.user)
                        current_owner_role = owner_profile.custom_role
                    except UserProfile.DoesNotExist:
                        pass
                        
                # Transferir propiedad si es anónimo o si pertenecía al Staff (Admin/Diseñador)
                if dep.user is None or current_owner_role in [UserProfile.Role.ADMIN, UserProfile.Role.DESIGNER]:
                    dep.user = self.request.user.id
                    dep.save()
                
                # Pasar el objeto completo al save_kwargs
                save_kwargs['deployment'] = dep
            except Deployment.DoesNotExist:
                pass

        # Lógica de Cupones B2C
        coupon_code = self.request.data.get('coupon_code')
        coupon_obj = None
        if coupon_code:
            from .models import Coupon
            try:
                coupon_obj = Coupon.objects.get(code__iexact=coupon_code)
                if coupon_obj.is_valid():
                    save_kwargs['coupon'] = coupon_obj
                else:
                    coupon_obj = None
            except Coupon.DoesNotExist:
                pass

        order = serializer.save(**save_kwargs)
        
        # Registrar y aplicar cálculo de descuento al Order si hubo cupón
        if coupon_obj:
            subtotal = float(order.subtotal_amount)
            discount_amount = 0.0
            if coupon_obj.discount_fixed > 0:
                discount_amount = float(coupon_obj.discount_fixed)
            elif coupon_obj.discount_percentage > 0:
                discount_amount = subtotal * (float(coupon_obj.discount_percentage) / 100.0)
            
            # Evitar descuentos mayores al subtotal
            if discount_amount > subtotal:
                discount_amount = subtotal

            order.discount_amount = discount_amount
            # Recalcular total (asumiendo que el frontend mandó el total original o debemos recalcular)
            order.total_amount = float(order.subtotal_amount) - discount_amount + float(order.tax_amount)
            order.save()
            
            # Incrementar uso del cupón
            coupon_obj.current_uses += 1
            coupon_obj.save()

        # Lógica de Comisiones: Solo si es POS y hay un vendedor diferente al cliente
        if order.origin == Order.OriginChoices.POS and order.vendor_id:
            if profile and profile.base_commission_rate > 0:
                commission_amount = (order.total_amount * profile.base_commission_rate) / 100
                Commission.objects.create(
                    order=order,
                    vendor_id=order.vendor_id,
                    amount=commission_amount,
                    percentage=profile.base_commission_rate
                )

    @action(detail=True, methods=['post'], url_path='send-email')
    def send_email_receipt(self, request, pk=None):
        from .tasks import send_receipt_email_task
        order = self.get_object()
        
        email = request.data.get('email')
        if email:
            order.customer_email = email
            order.save()
            
        if not order.customer_email:
            return Response({'error': 'La orden no tiene un correo de cliente asociado y no se proporcionó uno nuevo.'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            send_receipt_email_task.delay(order.id)
            return Response({'success': True, 'message': f'Recibo encolado exitosamente para enviarse a {order.customer_email}'})
        except Exception as e:
            return Response({'error': f'No se pudo encolar el correo: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], url_path='issue-cfdi')
    def issue_cfdi(self, request, pk=None):
        import uuid
        from django.core.exceptions import ValidationError as DjangoValidationError
        from rest_framework.exceptions import ValidationError
        from .models import Invoice
        from .serializers import InvoiceSerializer
        from .tasks import send_invoice_email_task
        
        order = self.get_object()
        
        # Validar si ya cuenta con factura
        if hasattr(order, 'invoice') and order.invoice:
            return Response({
                'error': 'Esta orden ya cuenta con una factura CFDI 4.0 timbrada.',
                'invoice': InvoiceSerializer(order.invoice).data
            }, status=status.HTTP_400_BAD_REQUEST)
            
        rfc = request.data.get('rfc', '').strip().upper()
        razon_social = request.data.get('razon_social', '').strip()
        codigo_postal = request.data.get('codigo_postal', '').strip()
        regimen_fiscal = request.data.get('regimen_fiscal', '').strip()
        uso_cfdi = request.data.get('uso_cfdi', '').strip()
        
        # Validaciones de reglas SAT para CFDI 4.0
        errors = {}
        if not rfc or len(rfc) not in [12, 13]:
            errors['rfc'] = 'El RFC debe tener exactamente 12 (Persona Moral) o 13 (Persona Física) caracteres.'
        if not razon_social:
            errors['razon_social'] = 'La Razón Social es requerida.'
        if not codigo_postal or len(codigo_postal) != 5 or not codigo_postal.isdigit():
            errors['codigo_postal'] = 'El Código Postal debe ser numérico y tener 5 dígitos.'
        if not regimen_fiscal or len(regimen_fiscal) != 3 or not regimen_fiscal.isdigit():
            errors['regimen_fiscal'] = 'El Régimen Fiscal debe ser una clave SAT válida de 3 dígitos.'
        if not uso_cfdi or len(uso_cfdi) != 3:
            errors['uso_cfdi'] = 'El Uso de CFDI debe ser una clave SAT válida de 3 caracteres.'
            
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            
        # ==============================================================================
        # PROVEEDOR DE FACTURACIÓN (PAC) - INFORMACIÓN PARA EL USUARIO
        # ==============================================================================
        # TODO: En producción, para realizar el timbrado real del CFDI 4.0 con el SAT:
        #
        # Proveedor Seleccionado: Facturapi (https://www.facturapi.com) u otro PAC (Quadrum/Finkok).
        # API Endpoint real de Facturapi para crear Facturas:
        #   POST https://api.facturapi.com/v1/invoices
        #
        # Autenticación:
        #   Mediante Header: Authorization: Bearer <API_KEY_PRIVADA>
        #
        # Estructura del payload sugerido para Facturapi:
        #   {
        #       "customer": {
        #           "legal_name": razon_social,
        #           "tax_id": rfc,
        #           "tax_system": regimen_fiscal,
        #           "address": { "zip": codigo_postal }
        #       },
        #       "items": [
        #           {
        #               "quantity": item.quantity,
        #               "product": {
        #                   "description": item.product.name,
        #                   "price": float(item.price_at_sale),
        #                   "product_key": "43231500",  # Clave SAT de Software / Licencias Digitales
        #                   "unit_key": "H87"           # Clave SAT de Unidad de Servicio (Pieza/Servicio)
        #               }
        #           } for item in order.items.all()
        #       ],
        #       "use": uso_cfdi,
        #       "payment_form": "01" if order.payment.payment_method == "CASH" else "04", # 01: Efectivo, 04: Tarjeta
        #       "payment_method": "PUE" # Pago en una sola exhibición
        #   }
        #
        # Al recibir la respuesta exitosa del PAC, se extraería el UUID y las URLs
        # oficiales del PDF y XML timbrados para guardarlas en la BD de ECOSYS.
        # ==============================================================================

        import sys
        import requests
        from django.conf import settings

        # Determinar si estamos en pruebas locales o si la key es de simulación
        is_testing = 'test' in sys.argv or any('pytest' in arg for arg in sys.argv)
        use_mock = is_testing or not getattr(settings, 'FACTURAPI_API_KEY', '') or settings.FACTURAPI_API_KEY in ['sk_test_placeholder', 'sk_test_tu_llave_aqui']

        if use_mock:
            # Simulación de Timbrado Mock
            sat_uuid = str(uuid.uuid4()).upper()
            pdf_url_mock = f"https://api.invtzn.local/media/invoices/{sat_uuid}.pdf"
            xml_url_mock = f"https://api.invtzn.local/media/invoices/{sat_uuid}.xml"
            
            try:
                invoice = Invoice.objects.create(
                    order=order,
                    rfc=rfc,
                    razon_social=razon_social,
                    codigo_postal=codigo_postal,
                    regimen_fiscal=regimen_fiscal,
                    uso_cfdi=uso_cfdi,
                    uuid=sat_uuid,
                    pdf_url=pdf_url_mock,
                    xml_url=xml_url_mock
                )
                
                # Intentar enviar correo con la factura
                if order.customer_email:
                    try:
                        send_invoice_email_task.delay(invoice.id)
                    except Exception as email_err:
                        import logging
                        logger = logging.getLogger(__name__)
                        logger.error(f"Error al encolar correo de factura simulada: {str(email_err)}")

                return Response({
                    'success': True,
                    'message': 'Factura timbrada exitosamente (Simulación CFDI 4.0 SAT) y recibo de factura encolado por correo.',
                    'invoice': InvoiceSerializer(invoice).data
                }, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                return Response({'error': f'Error al registrar la factura en base de datos: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Lógica real de Facturapi
        # 1. Mapear items de la orden
        items = []
        for item in order.items.all():
            product_type = item.product.product_type
            if product_type == 'PHYSICAL':
                product_key = '55121600'
                unit_key = 'H87'
            elif product_type == 'SERVICE':
                product_key = '82101600'
                unit_key = 'E48'
            else: # DIGITAL
                product_key = '43231500'
                unit_key = 'H87'
                
            tax_rate = float(item.product.tax_rate) if hasattr(item.product, 'tax_rate') else 0.16
            
            items.append({
                "quantity": item.quantity,
                "product": {
                    "description": item.product.name,
                    "price": float(item.price_at_sale),
                    "product_key": product_key,
                    "unit_key": unit_key,
                    "taxes": [
                        {
                            "rate": tax_rate,
                            "type": "IVA"
                        }
                    ],
                    "tax_included": True
                }
            })
            
        # 2. Mapear método de pago
        payment_form = "04"  # Default Tarjeta (Tarjeta de crédito)
        if hasattr(order, 'payment') and order.payment:
            method_str = order.payment.payment_method.upper()
            if method_str == "CASH":
                payment_form = "01"
            elif method_str == "BANK_TRANSFER":
                payment_form = "03"
            elif method_str == "CARD":
                payment_form = "04"
                
        # 3. Payload para Facturapi
        payload = {
            "customer": {
                "legal_name": razon_social,
                "tax_id": rfc,
                "tax_system": regimen_fiscal,
                "address": { "zip": codigo_postal }
            },
            "items": items,
            "use": uso_cfdi,
            "payment_form": payment_form,
            "payment_method": "PUE"
        }
        
        headers = {
            "Authorization": f"Bearer {settings.FACTURAPI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post("https://api.facturapi.com/v2/invoices", json=payload, headers=headers, timeout=15)
        except requests.exceptions.RequestException as e:
            return Response({
                'error': f'Error de conexión con Facturapi: {str(e)}'
            }, status=status.HTTP_502_BAD_GATEWAY)
            
        if response.status_code != 201:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', str(error_data))
            except:
                error_msg = response.text
            return Response({
                'error': f'Error devuelto por Facturapi (Código {response.status_code}): {error_msg}'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        response_data = response.json()
        invoice_id = response_data.get('id')
        sat_uuid = response_data.get('uuid')
        
        if not sat_uuid:
            sat_uuid = str(uuid.uuid4()).upper()
            
        pdf_url = f"https://api.facturapi.com/v2/invoices/{invoice_id}/pdf"
        xml_url = f"https://api.facturapi.com/v2/invoices/{invoice_id}/xml"
        
        try:
            invoice = Invoice.objects.create(
                order=order,
                rfc=rfc,
                razon_social=razon_social,
                codigo_postal=codigo_postal,
                regimen_fiscal=regimen_fiscal,
                uso_cfdi=uso_cfdi,
                uuid=sat_uuid,
                pdf_url=pdf_url,
                xml_url=xml_url
            )
            
            # Enviar correo con la factura
            if order.customer_email:
                try:
                    send_invoice_email_task.delay(invoice.id)
                except Exception as email_err:
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.error(f"Error al encolar correo de factura real: {str(email_err)}")

            return Response({
                'success': True,
                'message': 'Factura timbrada exitosamente con Facturapi y recibo de factura encolado por correo.',
                'invoice': InvoiceSerializer(invoice).data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': f'Error al registrar la factura en base de datos: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], url_path='resend-invoice')
    def resend_invoice(self, request, pk=None):
        from .tasks import send_invoice_email_task
        order = self.get_object()
        
        if not hasattr(order, 'invoice') or not order.invoice:
            return Response({'error': 'Esta orden no cuenta con una factura emitida para reenviar.'}, status=status.HTTP_400_BAD_REQUEST)
            
        email = request.data.get('email')
        if email:
            order.customer_email = email
            order.save()
            
        if not order.customer_email:
            return Response({'error': 'La orden no tiene un correo de cliente asociado y no se proporcionó uno nuevo.'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            send_invoice_email_task.delay(order.invoice.id)
            return Response({'success': True, 'message': f'Factura encolada para reenviarse al correo {order.customer_email}'})
        except Exception as e:
            return Response({'error': f'No se pudo encolar el reenvío de factura: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CashSessionViewSet(viewsets.ModelViewSet):
    serializer_class = CashSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        from profiles.models import UserProfile
        try:
            profile = UserProfile.objects.get(remote_auth_id=self.request.user.id)
            if profile.custom_role == UserProfile.Role.ADMIN:
                return CashSession.objects.all()
        except: pass
        return CashSession.objects.filter(user=self.request.user.id)

    def perform_create(self, serializer):
        from rest_framework.exceptions import ValidationError
        
        # Validar si ya hay una sesión abierta para este usuario en esta tienda
        store_id = self.request.data.get('store')
        if not store_id:
            raise ValidationError({'store': 'Debes especificar una tienda para abrir turno.'})
            
        existing_session = CashSession.objects.filter(
            user=self.request.user.id,
            store_id=store_id,
            is_open=True
        ).exists()
        
        if existing_session:
            raise ValidationError({'non_field_errors': 'Ya tienes un turno abierto en esta sucursal.'})
            
        serializer.save(user=self.request.user.id)

    @action(detail=True, methods=['post'], url_path='close')
    def close_session(self, request, pk=None):
        from django.utils import timezone
        from rest_framework.exceptions import ValidationError
        from decimal import Decimal
        
        session = self.get_object()
        if not session.is_open:
            return Response({'error': 'Esta sesión ya se encuentra cerrada.'}, status=400)
            
        closing_balance = request.data.get('closing_balance')
        if closing_balance is None:
            return Response({'error': 'El saldo de cierre (closing_balance) es requerido.'}, status=400)
            
        try:
            closing_balance = Decimal(str(closing_balance))
        except Exception:
            return Response({'error': 'Saldo de cierre inválido.'}, status=400)
            
        # Calcular ventas registradas en esta sucursal por este vendedor durante el turno
        completed_orders = Order.objects.filter(
            vendor_id=session.user,
            store=session.store,
            created_at__gte=session.opened_at,
            status=Order.StatusChoices.COMPLETED
        )
        
        # Sumar los montos de ventas completadas
        total_sales = sum(o.total_amount for o in completed_orders)
        expected_balance = session.opening_balance + total_sales
        difference = closing_balance - expected_balance
        
        # Cerrar la sesión
        session.closing_balance = closing_balance
        session.is_open = False
        session.closed_at = timezone.now()
        session.save()
        
        return Response({
            'session_id': session.id,
            'opened_at': session.opened_at,
            'closed_at': session.closed_at,
            'opening_balance': session.opening_balance,
            'closing_balance': session.closing_balance,
            'total_sales_amount': total_sales,
            'expected_closing_balance': expected_balance,
            'difference': difference,
            'is_open': session.is_open
        })

class CommissionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CommissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        from profiles.models import UserProfile
        try:
            profile = UserProfile.objects.get(remote_auth_id=self.request.user.id)
            if profile.custom_role == UserProfile.Role.ADMIN:
                return Commission.objects.all()
        except: pass
        return Commission.objects.filter(vendor_id=self.request.user.id)

from .models import Coupon
from .serializers import CouponSerializer

class CouponViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para la gestión de Cupones desde el panel B2B.
    Solo ADMIN y FRANCHISEE pueden acceder.
    """
    queryset = Coupon.objects.all().order_by('-id')
    serializer_class = CouponSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        profile = self._get_user_profile()
        if profile and profile.custom_role in [UserProfile.Role.ADMIN, UserProfile.Role.FRANCHISEE]:
            return Coupon.objects.all().order_by('-id')
        return Coupon.objects.none()

    def _get_user_profile(self):
        try:
            from profiles.models import UserProfile
            return UserProfile.objects.get(remote_auth_id=self.request.user.id)
        except:
            return None
