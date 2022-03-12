from django.db import models

from src.common.models import CoreModel
from src.shops.models import Shop


class StatusPayment(models.TextChoices):
    APPROVED = ('approved', 'Approved')
    PENDING = ('pending', 'Pending')
    ON_HOLD = ('on_hold', 'On hold')
    REJECTED = ('rejected', 'Rejected')
    PROCESSING = ('processing', 'Processing')


class Card(models.Model):
    number = models.CharField(max_length=50)
    expiry_month = models.CharField(max_length=50)
    expiry_year = models.CharField(max_length=50)
    cvv = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)


class Withdraw(CoreModel):
    amount = models.IntegerField()
    status = models.CharField(max_length=15, choices=StatusPayment.choices)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=100)
    details = models.CharField(max_length=254)
    note = models.CharField(max_length=100)
