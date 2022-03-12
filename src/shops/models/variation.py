from django.db import models


class Variation(models.Model):
    title = models.CharField(max_length=254)
    price = models.FloatField()
    sku = models.CharField(max_length=100)
    is_disable = models.BooleanField()
    sale_price = models.FloatField(null=True, blank=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.title


class VariationOption(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=254)
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE, related_name='options')

    def __str__(self):
        return self.name
