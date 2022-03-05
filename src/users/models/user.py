from django.contrib.auth.models import AbstractUser

from src.common.models import CoreModel


class User(AbstractUser, CoreModel):
    first_name = None
    last_name = None
