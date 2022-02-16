from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    roles = models.CharField(max_length=100, null=False)
    confirm_password = models.CharField(max_length=128, null=False)
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=150, null=False)

    REQUIRED_FIELDS = ['email', 'password', 'confirm_password', 'roles', 'first_name', 'last_name']
