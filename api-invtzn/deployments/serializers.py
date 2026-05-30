from rest_framework import serializers
from django.core.validators import RegexValidator
from .models import Deployment, SystemLog

class DeploymentSerializer(serializers.ModelSerializer):
    allowed_features = serializers.ReadOnlyField()
    slug = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        allow_null=True,
        validators=[
            RegexValidator(
                regex=r'^[a-z0-9-]+$',
                message="El slug solo puede contener letras minúsculas, números y guiones."
            )
        ]
    )

    product_tier = serializers.CharField(source='product.tier_level', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Deployment
        fields = '__all__'
        read_only_fields = ('user', 'status', 'is_paid', 'created_at', 'updated_at', 'allowed_features')

    def to_internal_value(self, data):
        from inventory.models import Product
        
        data_copy = data.copy() if hasattr(data, 'copy') else dict(data)
        product_id = data_copy.get('product')
        
        if product_id:
            try:
                if str(product_id) == '1' and not Product.objects.filter(id=1).exists():
                    default_product = Product.objects.filter(display_pcard=True).first()
                    if not default_product:
                        default_product = Product.objects.filter(product_type=Product.ProductType.DIGITAL, tier_level=Product.TierLevel.BASIC).first()
                    if not default_product:
                        default_product = Product.objects.filter(product_type=Product.ProductType.DIGITAL).first()
                    if not default_product:
                        default_product = Product.objects.first()
                    if default_product:
                        data_copy['product'] = default_product.id
            except Exception:
                pass

                
        return super().to_internal_value(data_copy)



    def validate_slug(self, value):
        if value:
            import re
            if not re.match(r'^[a-z0-9-]+$', value):
                raise serializers.ValidationError("El slug solo puede contener letras minúsculas, números y guiones.")
        return value

    def validate_custom_data(self, value):
        deployment = self.instance

        if not isinstance(value, dict):
            return value
            
        if not deployment:
            # En creación, permitimos omitir la validación de tiers ya que empieza vacío
            return value

        # Bypass de validación para administradores y diseñadores (staff)
        request = self.context.get('request')
        if request and request.user:
            if getattr(request.user, 'is_superuser', False):
                return value
            try:
                from profiles.models import UserProfile
                profile = UserProfile.objects.get(remote_auth_id=request.user.id)
                if profile.custom_role in [UserProfile.Role.ADMIN, UserProfile.Role.DESIGNER]:
                    return value
            except Exception:
                pass

        allowed = deployment.allowed_features
        blocks = value.get('blocks', [])

        # 1. Validar bloques dinámicos
        for block in blocks:
            b_type = block.get('type')
            if b_type == 'CountdownTimer' and not allowed.get('countdown_timer'):
                raise serializers.ValidationError("El bloque de Cuenta Regresiva (CountdownTimer) requiere plan Standard o Premium.")
            if b_type == 'TimelineBlock' and not allowed.get('timeline'):
                raise serializers.ValidationError("El bloque de Itinerario (TimelineBlock) requiere plan Premium.")

        # 2. Validar audio/música
        music = value.get('music', {})
        has_music_enabled = value.get('audioUrl') or value.get('has_music') or music.get('audioUrl') or music.get('has_music')
        if has_music_enabled and not allowed.get('background_music'):
            raise serializers.ValidationError("La música de fondo no está permitida en este plan.")

        # 3. Validar metadatos Open Graph personalizados
        has_custom_og = any(value.get(key) for key in ['og_title', 'og_description', 'og_image'])
        if has_custom_og and not allowed.get('custom_og'):
            raise serializers.ValidationError("La personalización de metadatos Open Graph requiere plan Premium.")

        return value


class SystemLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemLog
        fields = '__all__'
