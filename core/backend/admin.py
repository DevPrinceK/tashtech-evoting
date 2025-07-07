from django.contrib import admin

from accounts.models import User

from .models import *

admin.site.register(Candidate)
admin.site.register(Position)
admin.site.register(Election)
