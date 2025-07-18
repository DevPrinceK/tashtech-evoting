from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .manager import AccountManager


class User(AbstractBaseUser, PermissionsMixin):
    index_number = models.CharField(max_length=12, unique=True)
    fullname = models.CharField(max_length=60, null=True, blank=True)
    user_class = models.CharField(max_length=20, null=True, blank=True)
    house = models.CharField(max_length=20, null=True, blank=True)
    sex = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    total_votes_cast = models.IntegerField(default=0)
    already_voted = models.BooleanField(default=False)

    external_key = models.CharField(max_length=8, default='')

    is_staff = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'index_number'

    def __str__(self):
        return self.index_number
