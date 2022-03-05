# Register your models here.
from django.contrib.admin import ModelAdmin, register

from src.common.models import Attachment


@register(Attachment)
class AttachmentModelAdmin(ModelAdmin):
    pass
