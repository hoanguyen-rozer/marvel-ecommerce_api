from django.db import models

from src.common.models import CoreModel, Attachment


class TypeFeature(models.TextChoices):
    FIXED = ('fixed', 'Fixed')
    PERCENTAGE = ('percentage', 'Percentage')
    FREE_SHIPPING = ('free_shipping', 'Free Shipping')


class Coupon(CoreModel):
    code = models.CharField(max_length=50)
    description = models.CharField(max_length=254)
    type = models.CharField(max_length=50, choices=TypeFeature.choices)
    image = models.OneToOneField(Attachment, on_delete=models.SET_NULL, null=True, blank=True)
    is_valid = models.BooleanField(default=True)
    amount = models.IntegerField()
    active_from = models.CharField(max_length=100)
    expire_at = models.DateTimeField()
