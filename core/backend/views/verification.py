from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import View
from accounts.models import User

from core.utils.decorators import AdminOnly


class VerificationView(View):
    template = 'backend/verification.html'

    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        context = {}
        index_number = request.GET.get('index_number')
        voter = User.objects.filter(index_number=index_number, is_student=True).first()  # noqa
        if voter:
            messages.success(request, 'VOTER VERIFIED!')
            context = {'voter': voter}
            return render(request, self.template, context)
        else:
            print(index_number)
            if index_number is not None:
                messages.warning(request, 'VOTER NOT VERIFIED!')
            return render(request, self.template, context)
