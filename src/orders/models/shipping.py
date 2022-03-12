from django.db import models

from src.common.models import CoreModel
from src.orders.models.coupon import TypeFeature


class Shipping(CoreModel):
    name = models.CharField(max_length=254)
    amount = models.IntegerField()
    is_global = models.BooleanField()
    type = models.CharField(max_length=50, choices=TypeFeature.choices)
