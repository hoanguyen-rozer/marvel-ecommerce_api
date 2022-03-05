# Register your models here.
from django.contrib.admin import register, ModelAdmin

from src.users.models import User, Profile, Address, UserAddress


@register(User)
class UserModelAdmin(ModelAdmin):
    pass


@register(Profile)
class ProfileModelAdmin(ModelAdmin):
    pass


@register(Address)
class AddressModelAdmin(ModelAdmin):
    pass


@register(UserAddress)
class UserAddressModelAdmin(ModelAdmin):
    pass
