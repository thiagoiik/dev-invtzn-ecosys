from rest_framework import serializers
from .models import Product, Template

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ['vue_component_name', 'default_config']

class ProductSerializer(serializers.ModelSerializer):
    template = TemplateSerializer(source='template_config', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'