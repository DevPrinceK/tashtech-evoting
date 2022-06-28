from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .manager import AccountManager


class User(AbstractBaseUser, PermissionsMixin):
    index_number = models.CharField(max_length=12, unique=True)
    fullname = models.CharField(max_length=60, null=True, blank=True)
    user_class = models.CharField(max_length=20, null=True, blank=True)
    house = models.CharField(max_length=20, null=True, blank=True)
    # voted for senior prefects
    voted_for_sp = models.BooleanField(default=False)
    voted_for_gp = models.BooleanField(default=False)
    # voted for compound overseers
    voted_for_cob = models.BooleanField(default=False)
    voted_for_cog = models.BooleanField(default=False)
    # voted for spaorts & games prefects
    voted_for_sgpb = models.BooleanField(default=False)
    voted_for_sgpg = models.BooleanField(default=False)
    # voted for dining hall prefects
    voted_for_dhpb = models.BooleanField(default=False)
    voted_for_dhpg = models.BooleanField(default=False)
    # voted for entertainment prefects
    voted_for_ecpb = models.BooleanField(default=False)
    voted_for_ecpg = models.BooleanField(default=False)
    # voted for library prefects
    voted_for_lpb = models.BooleanField(default=False)
    voted_for_lpg = models.BooleanField(default=False)
    # voted for chapel stewards
    voted_for_csb = models.BooleanField(default=False)
    voted_for_csg = models.BooleanField(default=False)
    # voted for preps prefects
    voted_for_ppb = models.BooleanField(default=False)
    voted_for_ppg = models.BooleanField(default=False)
    # voted for health sanitations prefects
    voted_for_hspb = models.BooleanField(default=False)
    voted_for_hspg = models.BooleanField(default=False)
    # voted fir house prefects
    voted_for_hpb = models.BooleanField(default=False)
    voted_for_hpg = models.BooleanField(default=False)
    # voted for all positions
    voted_for_all = models.BooleanField(default=False)

    external_key = models.CharField(max_length=8, default='')

    is_staff = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'index_number'

    def __str__(self):
        return self.index_number
