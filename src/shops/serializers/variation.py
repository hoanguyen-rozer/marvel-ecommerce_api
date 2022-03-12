from rest_framework import serializers

from src.shops.models import Variation, VariationOption


class VariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variation
        fields = ('title', 'price', 'sku', 'is_disable', 'sale_price', 'quantity')


class VariationOptionSerializer(serializers.ModelSerializer):
    variation = VariationSerializer()

    class Meta:
        model = VariationOption
        fields = ('name', 'value', 'variation')
