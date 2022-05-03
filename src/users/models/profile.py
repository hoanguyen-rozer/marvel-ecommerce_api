from django.conf import settings
from django.db import models

from src.common.models import CoreModel, Attachment


class Profile(CoreModel):
    """
    Extra fields of user profile
    """
    avatar = models.OneToOneField(Attachment, on_delete=models.SET_NULL, null=True, blank=True)
    bio = models.CharField(max_length=255, null=True, blank=True)
    contact = models.CharField(max_length=15, null=True, blank=True)
    customer = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
