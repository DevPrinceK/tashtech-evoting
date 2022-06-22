from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


class LandingPageView(View):
    template = 'accounts/landing_page.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template, {})


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
                return redirect('voting:landing_page')
            elif user.is_staff or user.is_superuser:
                messages.success(request, 'Login successful')
                return redirect('backend:index')
        else:
            messages.error(request, 'Login failed')
            return redirect('accounts:login')


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'Logout successful')
        return redirect('accounts:login')
