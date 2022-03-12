from rest_framework import serializers

from src.common.serializers import AttachmentSerializer
from src.shops.models import TypeSetting, Type, Banner, Tag, Category
from src.shops.serializers.product import ProductUpdateSerializer


class TypeSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeSetting
        fields = ('in_home', 'layout_type', 'product_card')


class BannerSerializer(serializers.ModelSerializer):
    image = AttachmentSerializer()

    class Meta:
        model = Banner
        fields = ('title', 'description', 'image')


class TypeSerializer(serializers.ModelSerializer):
    image = AttachmentSerializer(required=False)
    banners = BannerSerializer(many=True, required=False)
    settings = TypeSettingSerializer(required=False)

    class Meta:
        model = Type
        fields = ('name', 'slug', 'image', 'icon', 'promotion_sliders', 'settings', 'created_at', 'updated_at')


class TagSerializer(serializers.ModelSerializer):
    type = TypeSerializer()
    products = ProductUpdateSerializer(many=True)

    class Meta:
        model = Tag
        fields = ('name', 'details', 'image', 'icon', 'type', 'products', 'created_at', 'updated_at')


class CategorySerializer(serializers.ModelSerializer):
    image = AttachmentSerializer(required=False)
    type = TypeSerializer(required=False)

    class Meta:
        model = Category
        fields = ('name', 'slug', 'details', 'image', 'icon', 'type', 'created_at', 'updated_at')
