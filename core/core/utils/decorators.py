from django.shortcuts import redirect
from django.contrib import messages


class AdminOnly(object):
    '''Ensures that only admins can access page'''

    def __init__(self, original_method):
        self.original_method = original_method

    def __call__(self, request, *args,  **kwargs):
        if request.user.is_authenticated:
            if (request.user.is_superuser or request.user.is_staff):
                return self.original_method(request, *args, **kwargs)
            else:
                messages.error(
                    request, 'Unauthorised Access is Prohibited!')
                return redirect('accounts:login')
        else:
            messages.error(
                request, 'Sorry, You must login to continue. ')
            return redirect('accounts:login')


class MustLogin(object):
    '''Ensures that user is authenticated'''

    def __init__(self, original_method):
        self.original_method = original_method

    def __call__(self, request, *args,  **kwargs):
        if request.user.is_authenticated:
            if (request.user.is_superuser or request.user.is_staff or request.user.is_student):  # noqa
                return self.original_method(request, *args, **kwargs)
            else:
                messages.error(
                    request, 'Login Required!')
                return redirect('accounts:login')
        else:
            messages.error(
                request, 'Sorry, You must login to continue!')
            return redirect('accounts:login')
