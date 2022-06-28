from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from backend.models import Election


class LandingPageView(View):
    template = 'accounts/landing_page.html'

    def get(self, request, *args, **kwargs):
        current_election = Election.objects.filter(is_active=True).order_by('created_at').first()  # noqa
        context = {'current_election': current_election}
        return render(request, self.template, context)


class LoginView(View):
    '''Implements login functionality'''
    template = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template, {})

    def post(self, request, *args, **kwargs):
        index_number = request.POST.get('index_number')
        pin = request.POST.get('pin')
        user = authenticate(index_number=index_number, password=pin)
        if user:
            login(request, user)
            if user.is_student:
                messages.success(request, 'Login successful')
                return redirect('voting:instructions')
            elif user.is_staff or user.is_superuser:
                messages.success(request, 'Login successful')
                return redirect('backend:index')
        else:
            messages.error(request, 'Login failed')
            return redirect('accounts:login')


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('accounts:login')
