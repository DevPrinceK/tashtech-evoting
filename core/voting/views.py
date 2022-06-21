from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect

from core.utils.decorators import MustLogin


class LandinPageView(View):
    template = 'voting/landing_page.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template, {})
