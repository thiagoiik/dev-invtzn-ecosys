from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import BankSyncLog
from .serializers import BankSyncLogSerializer
from sales.models import Order, PaymentTransaction
from django.utils import timezone
from integrations.stripe_provider import StripeProvider

class ReconciliationViewSet(viewsets.ModelViewSet):
    queryset = BankSyncLog.objects.all().order_by('-timestamp')
    serializer_class = BankSyncLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        from profiles.models import UserProfile
        try:
            profile = UserProfile.objects.get(remote_auth_id=self.request.user.id)
            if profile.custom_role in [UserProfile.Role.ADMIN, UserProfile.Role.FRANCHISEE, UserProfile.Role.MANAGER]:
                return BankSyncLog.objects.all().order_by('-timestamp')
        except: pass
        return BankSyncLog.objects.none()

    @action(detail=False, methods=['post'], url_path='sync')
    def sync_order(self, request):
        bank_log_id = request.data.get('bank_log_id')
        order_id = request.data.get('order_id')

        if not bank_log_id or not order_id:
            return Response({'error': 'Se requiere bank_log_id y order_id'}, status=400)

        try:
            bank_log = BankSyncLog.objects.get(id=bank_log_id, is_reconciled=False)
            order = Order.objects.get(id=order_id, status=Order.StatusChoices.PENDING)
            
            if bank_log.amount < order.total_amount:
                return Response({'error': 'El monto del banco es menor al total de la orden'}, status=400)

            order.status = Order.StatusChoices.COMPLETED
            order.save()

            PaymentTransaction.objects.create(
                order=order,
                provider='BANK_SYNC',
                payment_method='BANK_TRANSFER',
                transaction_id=bank_log.external_id,
                success=True
            )

            bank_log.is_reconciled = True
            bank_log.reconciled_at = timezone.now()
            bank_log.order = order
            bank_log.save()

            return Response({'success': f'Orden #{order.id} conciliada con éxito'})

        except BankSyncLog.DoesNotExist:
            return Response({'error': 'Movimiento bancario no encontrado o ya conciliado'}, status=404)
        except Order.DoesNotExist:
            return Response({'error': 'Orden no encontrada o no está pendiente'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

    @action(detail=False, methods=['post'], url_path='simulate-webhook')
    def simulate_webhook(self, request):
        amount = request.data.get('amount', 100.00)
        external_id = f"STP-{timezone.now().timestamp()}"
        
        log = BankSyncLog.objects.create(
            external_id=external_id,
            amount=amount,
            sender_name="CLIENTE SIMULADO S.A.",
            sender_bank="BBVA",
            description="Pago de factura",
            timestamp=timezone.now()
        )
        return Response(BankSyncLogSerializer(log).data)

    @action(detail=False, methods=['get'], url_path='debug-stripe')
    def debug_stripe(self, request):
        StripeProvider._set_api_key()
        import stripe
        try:
            # Prueba 1: Recuperar información de la cuenta propia
            my_account = stripe.Account.retrieve()
            
            # Prueba 2: Intentar crear la cuenta más simple posible (Standard)
            # test_account = stripe.Account.create(type="standard")
            
            return Response({
                'status': 'API Key válida',
                'account_id': my_account.id,
                'business_name': my_account.settings.dashboard.display_name,
                'charges_enabled': my_account.charges_enabled,
                'details_submitted': my_account.details_submitted
            })
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class StripeWebhookView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        
        success, message = StripeProvider.handle_webhook(payload, sig_header)
        
        if success:
            return Response({'status': 'success'}, status=200)
        else:
            return Response({'error': message}, status=400)
