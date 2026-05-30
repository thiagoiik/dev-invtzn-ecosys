from rest_framework import serializers
from .models import Product, Store

class ProductSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.SerializerMethodField()
    template_config = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_thumbnail_url(self, obj):
        if obj.template_slug:
            from inventory.models import DesignTemplate
            template = DesignTemplate.objects.filter(slug=obj.template_slug, is_active=True).first()
            if template and template.thumbnail_url:
                return template.thumbnail_url
            
            from deployments.models import Deployment
            try:
                dep = Deployment.objects.filter(slug=obj.template_slug).first()
                if dep and dep.custom_data:
                    return dep.custom_data.get('og_image') or dep.custom_data.get('cover', {}).get('coverPhoto')
            except Exception:
                pass
        return None

    def get_template_config(self, obj):
        if obj.template_slug:
            from deployments.models import Deployment
            try:
                dep = Deployment.objects.filter(slug=obj.template_slug).first()
                if dep:
                    return dep.custom_data
            except Exception:
                pass
        return None


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'