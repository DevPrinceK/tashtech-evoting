from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .manager import AccountManager


class User(AbstractBaseUser, PermissionsMixin):
    index_number = models.CharField(max_length=12, unique=True)
    fullname = models.CharField(max_length=60, null=True, blank=True)
    form = models.CharField(max_length=20, null=True, blank=True)
    user_class = models.CharField(max_length=20, null=True, blank=True)
    is_student = models.BooleanField(default=False)
    is_done_voting = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'index_number'

    def __str__(self):
        return self.index_number
