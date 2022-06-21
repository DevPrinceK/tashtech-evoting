from django.db import models

class User(models.Model):
    index_number = models.CharField(max_length=12, unique=True)
    fullname = models.CharField(max_length=60)
    form = models.CharField(max_length=20)
    user_class = models.CharField(max_length=20)
    is_student = models.BooleanField(default=False)
    is_done_voting = models.BooleanField(default=False)

    def __str__(self):
        return self.index_number
