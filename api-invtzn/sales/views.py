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

    @action(detail=True, methods=['post'], url_path='complete-pos')
    def complete_pos_order(self, request, pk=None):
        from django.utils import timezone
        from .models import PaymentTransaction, CashSession
        
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
        
        return Response({
            'success': True,
            'order_id': order.id,
            'status': order.status,
            'payment_method': payment_method
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
                # Reclamar si es anónimo
                if dep.user is None:
                    dep.user = self.request.user.id
                    dep.save()
                
                # Pasar el objeto completo al save_kwargs
                save_kwargs['deployment'] = dep
            except Deployment.DoesNotExist:
                pass

        order = serializer.save(**save_kwargs)
        
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
