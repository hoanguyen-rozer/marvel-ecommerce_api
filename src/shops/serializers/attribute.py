from rest_framework import serializers

from src.shops.models import Attribute, AttributeValue


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = ('value', 'meta')


class AttributeSerializer(serializers.ModelSerializer):
    values = AttributeValueSerializer(many=True)

    class Meta:
        model = Attribute
        fields = ('name', 'shop', 'slug', 'values')
