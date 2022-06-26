from django.shortcuts import render
from django.views import View

from backend.models import Election


class IndexView(View):
    template = 'backend/index.html'

    def get(self, request, *args, **kwargs):
        current_election = Election.objects.filter(is_active=True).order_by('created_at').first()  # noqa
        context = {'current_election': current_election}
        return render(request, self.template, context)
