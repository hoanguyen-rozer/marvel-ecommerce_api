from django.db import models

from src.common.models import Attachment, CoreModel


class TypeSetting(models.Model):
    """
    Settings relate user interface of shops
    """
    in_home = models.BooleanField()
    layout_type = models.CharField(max_length=100)
    product_card = models.CharField(max_length=100)


class Type(CoreModel):
    name = models.CharField(max_length=254)
    slug = models.SlugField()
    image = models.OneToOneField(Attachment, on_delete=models.SET_NULL, null=True, blank=True)
    icon = models.CharField(max_length=254)
    promotional_sliders = models.ManyToManyField(Attachment, related_name='types')
    settings = models.OneToOneField(TypeSetting, on_delete=models.SET_NULL, null=True, blank=True)


class Banner(models.Model):
    """
    Banners in shop's user interface
    """
    title = models.CharField(max_length=254, null=True, blank=True)
    description = models.CharField(max_length=254, null=True, blank=True)
    image = models.OneToOneField(Attachment, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='banners')


class Tag(CoreModel):
    name = models.CharField(max_length=254)
    slug = models.SlugField()
    # parent =
    details = models.CharField(max_length=254)
    image = models.OneToOneField(Attachment, on_delete=models.SET_NULL, null=True, blank=True)
    icon = models.CharField(max_length=100)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='tags')


class Category(CoreModel):
    """
    Categories of products
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    details = models.CharField(max_length=254, null=True, blank=True)
    image = models.OneToOneField(Attachment, on_delete=models.SET_NULL, null=True, blank=True)
    icon = models.CharField(max_length=100, null=True, blank=True)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True, blank=True)
