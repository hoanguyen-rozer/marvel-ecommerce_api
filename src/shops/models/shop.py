from django.conf import settings
from django.db import models

from src.common.models import CoreModel, Attachment, Location
from src.users.models import UserAddress


class Shop(CoreModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    # orders_count =
    # products_count =
    # balance =
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.CharField(max_length=255, null=True, blank=True)
    cover_image = models.OneToOneField(Attachment, on_delete=models.SET_NULL, null=True)
    logo = models.OneToOneField(Attachment, on_delete=models.SET_NULL, null=True)
    address = models.OneToOneField(UserAddress, on_delete=models.PROTECT)


class ShopSetting(models.Model):
    contact = models.CharField(max_length=15, null=True, blank=True)
    location = models.OneToOneField(Location, on_delete=models.SET_NULL, null=True)
    website = models.CharField(max_length=100, null=True, blank=True)
