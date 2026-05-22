from rest_framework import serializers
from .models import Order, CashSession, Commission, OrderItem, Invoice, ShippingAddress
from inventory.models import Product

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ('recipient_name', 'address_line1', 'address_line2', 'city', 'state', 'postal_code', 'phone')

class OrderItemSerializer(serializers.ModelSerializer):
    serial_keys = serializers.SerializerMethodField()
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_is_physical = serializers.BooleanField(source='product.is_physical', read_only=True)

    class Meta:
        model = OrderItem
        fields = ('product', 'quantity', 'price_at_sale', 'serial_keys', 'product_name', 'product_is_physical')

    def get_serial_keys(self, obj):
        return list(obj.serial_keys.values_list('key_value', flat=True))

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(required=False)
    items = OrderItemSerializer(many=True, required=False)
    invoice = InvoiceSerializer(read_only=True, required=False)
    shipping_address = ShippingAddressSerializer(required=False, allow_null=True)
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True, required=False
    )
    
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('status', 'created_at', 'updated_at')

    def validate(self, attrs):
        request = self.context.get('request')
        discount_amount = attrs.get('discount_amount', 0)
        
        if discount_amount > 0:
            if not request or not request.user or not request.user.is_authenticated:
                raise serializers.ValidationError({"discount_amount": "No autenticado."})
            
            try:
                from profiles.models import UserProfile
                profile = UserProfile.objects.get(remote_auth_id=request.user.id)
                role = profile.custom_role
            except UserProfile.DoesNotExist:
                role = 'CLIENT'
                
            if role not in ['ADMIN', 'FRANCHISEE']:
                raise serializers.ValidationError(
                    {"discount_amount": "No tienes permisos para aplicar descuentos directos."}
                )
                
        return attrs

    def create(self, validated_data):
        shipping_address_data = validated_data.pop('shipping_address', None)
        items_data = validated_data.pop('items', [])
        legacy_product = validated_data.pop('product', None)
        
        order = Order.objects.create(**validated_data)
        
        if shipping_address_data:
            ShippingAddress.objects.create(order=order, **shipping_address_data)
            
        if items_data:
            for item_data in items_data:
                product = item_data['product']
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item_data['quantity'],
                    price_at_sale=item_data['price_at_sale']
                )
        elif legacy_product:
            OrderItem.objects.create(
                order=order,
                product=legacy_product,
                quantity=1,
                price_at_sale=order.total_amount
            )
            
        return order

class CashSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashSession
        fields = '__all__'
        read_only_fields = ('opened_at', 'is_open')

class CommissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commission
        fields = '__all__'
