from django.contrib import admin

from src.shops.models import Shop, ShopSetting


@admin.register(Shop)
class ShopModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name',)
    }


@admin.register(ShopSetting)
class ShopSettingModelAdmin(admin.ModelAdmin):
    pass
