from django.db import models

from src.common.models import CoreModel
from src.shops.models import Shop


class Attribute(CoreModel):
    """
    Multiple attribute relate products in shops
    """
    name = models.CharField(max_length=254)
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(max_length=254)

    def __str__(self):
        return self.name


class AttributeValue(CoreModel):
    """
    Class contain value of attribute
    """
    # shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True)
    value = models.CharField(max_length=254)
    meta = models.CharField(max_length=254, null=True, blank=True)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='values')

    def __str__(self):
        return self.value + self.meta if self.meta else ''
