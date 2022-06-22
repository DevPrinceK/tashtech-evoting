from django.contrib.auth.models import BaseUserManager


class AccountManager(BaseUserManager):
    '''Custom User Account Creation Manager'''

    def create_user(self, index_number, password, **kwargs):
        user = self.model(index_number=index_number, password=password, **kwargs)  # noqa
        user.set_password(password)
        user.is_student = True
        user.save()
        return user

    def create_superuser(self, index_number, password, **kwargs):
        user = self.create_user(index_number=index_number, password=password, **kwargs)  # noqa
        user.is_superuser = True
        user.is_staff = True
        user.is_student = False
        user.save()
        return user
