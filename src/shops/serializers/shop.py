from django.utils.text import slugify
from rest_framework import serializers

from src.common.models import Attachment, Location
from src.common.serializers import AttachmentSerializer, LocationSerializer
from src.shops.models import Shop, ShopSetting
from src.users.models import UserAddress
from src.users.serializers import UserAddressSerializer


class ShopSettingSerializer(serializers.ModelSerializer):
    location = LocationSerializer(required=False)

    class Meta:
        model = ShopSetting
        fields = ('contact', 'location', 'website')


class ShopSerializer(serializers.ModelSerializer):
    cover_image = AttachmentSerializer(required=False)
    logo = AttachmentSerializer(required=False)
    address = UserAddressSerializer()
    settings = ShopSettingSerializer(required=False)
    orders_count = serializers.SerializerMethodField()
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Shop
        fields = ('owner', 'name', 'slug', 'description', 'cover_image', 'logo', 'is_active', 'address', 'settings',
                  'orders_count', 'products_count', 'created_at', 'updated_at')
        extra_kwargs = {
            'slug': {
                'read_only': True
            }
        }

    def get_orders_count(self, obj):
        return 15

    def get_products_count(self, obj):
        return 15

    def create(self, validated_data):
        cover_image_data = validated_data.pop('cover_image')
        logo_data = validated_data.pop('logo')
        address_data = validated_data.pop('address')
        settings_data = validated_data.pop('settings')

        shop_name = validated_data.get('name')
        slug = slugify(shop_name)
        cover_image_attachment = None
        logo_attachment = None
        shop_setting = None
        if cover_image_data:
            cover_image_attachment = Attachment.objects.create(**cover_image_data)
        if logo_data:
            logo_attachment = Attachment.objects.create(**logo_data)
        address = UserAddress.objects.create(**address_data)
        if settings_data:
            location_data = settings_data.pop('location')
            location = Location.objects.create(**location_data)
            shop_setting = ShopSetting.objects.create(**settings_data, location=location)
        shop = Shop.objects.create(**validated_data, slug=slug, cover_image=cover_image_attachment,
                                   logo=logo_attachment, address=address, settings=shop_setting)
        return shop

    def update(self, instance, validated_data):
        print('DATA: ', validated_data)
