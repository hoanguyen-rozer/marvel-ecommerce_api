from rest_framework import serializers

from src.users.models import UserAddress, Address


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ('zip', 'city', 'country', 'street_address')


class AddressSerializer(serializers.ModelSerializer):
    address = UserAddressSerializer()

    class Meta:
        model = Address
        fields = ('title', 'type', 'default', 'address', 'created_at', 'updated_at')
