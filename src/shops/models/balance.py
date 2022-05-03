from django.db import models

from src.shops.models import Shop


class PaymentInfo(models.Model):
    account = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    bank = models.CharField(max_length=100)


class Balance(models.Model):
    """
    General financial information
    """
    admin_commission_rate = models.FloatField()
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    total_earnings = models.FloatField()
    withdrawn_amount = models.FloatField()
    current_balance = models.FloatField()
    payment_info = models.OneToOneField(PaymentInfo, on_delete=models.SET_NULL, null=True)

