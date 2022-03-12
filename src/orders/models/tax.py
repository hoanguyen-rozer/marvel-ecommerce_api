from django.db import models

from src.common.models import CoreModel


class Tax(CoreModel):
    name = models.CharField(max_length=254)
    rate = models.FloatField()
    is_global = models.BooleanField()
    country = models.CharField(max_length=100, null=True, blank=True)
    zip = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    priority = models.IntegerField()
    on_shipping = models.BooleanField()
