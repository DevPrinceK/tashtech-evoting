from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


class LoginView(View):
    template = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template, {})

    def post(self, request, *args, **kwargs):
        index_number = request.POST.get('index_number')
        pin = request.POST.get('pin')
        user = authenticate(index_number=index_number, pin=pin)
        if user:
            login(request, user)
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
