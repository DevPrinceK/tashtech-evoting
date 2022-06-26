from django.shortcuts import render
from django.views import View

from backend.models import Candidate, Election, Position
from core.utils.constants import PortfolioName


class IndexView(View):
    template = 'backend/index.html'

    def get(self, request, *args, **kwargs):
        current_election = Election.objects.filter(is_active=True).order_by('created_at').first()  # noqa
        positions = Position.objects.all().order_by('-id')
        src_presidents = Candidate.objects.filter(position__name=PortfolioName.SP.value).order_by('ballot_number')  # noqa

        context = {
            'current_election': current_election,
            'positions': positions,
            'src_presidents': src_presidents,
        }
        return render(request, self.template, context)
