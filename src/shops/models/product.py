from django.db import models

from src.common.models import CoreModel, Attachment
from src.orders.models import OrderProductPivot
from src.shops.models import Type, Category, Tag, AttributeValue, Shop


class Product(CoreModel):
    class ProductType(models.TextChoices):
        SIMPLE = ('simple', 'Simple')
        VARIABLE = ('variable', 'Variable')

    class ProductStatus(models.TextChoices):
        PUBLISH = ('publish', 'Publish')
        DRAFT = ('draft', 'Draft')

    name = models.CharField(max_length=254)
    slug = models.SlugField()
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='products')
    product_type = models.CharField(max_length=10, choices=ProductType.choices)
    categories = models.ManyToManyField(Category, related_name='products')
    tags = models.ManyToManyField(Tag, related_name='products')
    variations = models.ManyToManyField(AttributeValue, blank=True)
    variation_options = models.ManyToManyField(to='shops.Variation', blank=True)
    pivot = models.OneToOneField(OrderProductPivot, on_delete=models.SET_NULL, null=True, blank=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products')
    # related_products[...]
    description = models.TextField()
    in_stock = models.BooleanField(default=True)
    is_taxable = models.BooleanField(default=True)
    sale_price = models.FloatField(null=True, blank=True)
    max_price = models.FloatField(null=True, blank=True)
    min_price = models.FloatField(null=True, blank=True)
    sku = models.CharField(max_length=100, null=True, blank=True)
    gallery = models.ManyToManyField(Attachment, blank=True,related_name='products_gallery')
    image = models.OneToOneField(Attachment, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10, choices=ProductStatus.choices, default=ProductStatus.PUBLISH)

    height = models.CharField(max_length=100, null=True, blank=True)
    length = models.CharField(max_length=100, null=True, blank=True)
    width = models.CharField(max_length=100, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    quantity = models.IntegerField()
    unit = models.CharField(max_length=100)
