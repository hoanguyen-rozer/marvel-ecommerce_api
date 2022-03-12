from rest_framework import serializers

from src.orders.models import OrderProductPivot, OrderStatus, Order
from src.users.serializers import UserAddressSerializer


class OrderProductPivotSerializer(serializers.ModelSerializer):
    variation_option = serializers.PrimaryKeyRelatedField(required=False)

    class Meta:
        model = OrderProductPivot
        fields = ('variation_option', 'order_quantity', 'unit_price', 'subtotal')


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = ('name', 'color', 'serial', 'created_at', 'updated_at')


class OrderSerializer(serializers.ModelSerializer):
    # shop =
    # coupon =
    status = OrderStatusSerializer()
    # card =
    billing_address = UserAddressSerializer(required=False)
    shipping_address = UserAddressSerializer(required=False)

    class Meta:
        model = Order
        fields = (
            'shop', 'coupon', 'status', 'amount', 'sale_tax', 'total', 'paid_total', 'payment_id', 'payment_gateway',
            'discount', 'delivery_fee', 'delivery_time', 'card', 'billing_address', 'shipping_address')
