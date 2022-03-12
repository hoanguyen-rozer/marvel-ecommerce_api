from rest_framework import serializers

from src.shops.models import Product


class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'name', 'type', 'product_type', 'variations', 'shop', 'description', 'in_stock', 'is_taxable', 'sale_price',
            'max_price', 'min_price', 'sku', 'gallery', 'image', 'status', 'height', 'length', 'width', 'price',
            'quantity',
            'unit', 'categories', 'tags'
        )
