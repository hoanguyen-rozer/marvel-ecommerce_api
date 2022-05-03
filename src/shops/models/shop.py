from django.conf import settings
from django.db import models

from src.common.models import CoreModel, Attachment, Location
from src.users.models import UserAddress


class ShopSetting(models.Model):
    """
    Class contain info relate contact
    """
    contact = models.CharField(max_length=15, null=True, blank=True)
    location = models.OneToOneField(Location, on_delete=models.SET_NULL, null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.website} - {self.contact} - {self.location.city}"


class Shop(CoreModel):
    """
    Class contain main info relate shop
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    # orders_count =
    # products_count =
    # balance =
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    cover_image = models.OneToOneField(Attachment, on_delete=models.SET_NULL, null=True, blank=True)
    logo = models.OneToOneField(Attachment, on_delete=models.SET_NULL, null=True, related_name='shop_logo')
    address = models.OneToOneField(UserAddress, on_delete=models.PROTECT)
    settings = models.OneToOneField(ShopSetting, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.owner.username}"
