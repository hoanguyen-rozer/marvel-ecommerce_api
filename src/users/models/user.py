from django.contrib.auth.models import AbstractUser

from src.common.models import CoreModel


class User(AbstractUser, CoreModel):
    """
    Custom user model without default fields are first_name and last_name
    """
    first_name = None
    last_name = None
