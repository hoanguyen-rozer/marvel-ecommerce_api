from django.conf import settings
from django.db import models

from src.common.models import CoreModel


class AddressType(models.TextChoices):
    BILLING = 'billing', 'Billing'
    SHIPPING = 'shipping', 'Shipping'


class UserAddress(models.Model):
    """
    Generic class contain fields relate address of an object
    """
    street_address = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.street_address}, {self.country}, {self.city} - {self.zip}"


class Address(CoreModel):
    """
    Class define addresses of one user
    """
    title = models.CharField(max_length=255)
    default = models.BooleanField(default=False)
    address = models.OneToOneField(UserAddress, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=AddressType.choices)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='address')

    def __str__(self):
        return f"{self.customer.username} - {self.title} - {self.address}"
