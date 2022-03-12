from django.db import models

from config.settings import AUTH_USER_MODEL
from src.common.models import CoreModel
from src.orders.models import Coupon
from src.shops.models import Shop
from src.users.models import UserAddress


class OrderProductPivot(models.Model):
    variation_option = models.ForeignKey(to='shops.VariationOption', on_delete=models.SET_NULL, null=True,
                                         blank=True)
    order_quantity = models.IntegerField()
    unit_price = models.IntegerField()
    subtotal = models.FloatField()


class OrderStatus(CoreModel):
    name = models.CharField(max_length=254)
    color = models.CharField(max_length=100)
    serial = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.serial}"


class Order(CoreModel):
    class PaymentGateWay(models.TextChoices):
        STRIPE = ('stripe', 'Stripe')
        COD = ('cod', 'COD')

    tracking_number = models.CharField(max_length=100)
    customer = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.PROTECT)
    status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, null=True)
    amount = models.IntegerField()
    sales_tax = models.FloatField()
    total = models.FloatField()
    paid_total = models.FloatField()
    payment_id = models.CharField(max_length=100)
    payment_gateway = models.CharField(max_length=10, choices=PaymentGateWay.choices, default=PaymentGateWay.COD)
    coupon = models.ManyToManyField(Coupon, related_name='orders')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    discount = models.FloatField(null=True, blank=True)
    delivery_fee = models.FloatField(null=True, blank=True)
    delivery_time = models.DateTimeField()
    products = models.ManyToManyField(to='shops.Product', related_name='orders')
    billing_address = models.ForeignKey(UserAddress, on_delete=models.DO_NOTHING, related_name='orders_billing')
    shipping_address = models.ForeignKey(UserAddress, on_delete=models.DO_NOTHING, related_name='orders_shipping')
