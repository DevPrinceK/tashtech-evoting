from django.shortcuts import render
from django.views import View
from accounts.models import User

from backend.models import Candidate, Election, Position
from django.utils.decorators import method_decorator
from core.utils.constants import House, PositionName
from core.utils.decorators import AdminOnly


class NewDashboardView(View):
    '''New view for displaying the dashboard'''
    template = 'backend/dashboard.html'

    @method_decorator(AdminOnly)
    def get(self, request, *args, **kwargs):
        current_election = Election.objects.all().first()
        candidates = Candidate.objects.all().order_by('position__precedence', 'ballot_number')  # noqa
        total_votes_cast = User.objects.filter(is_student=True, already_voted=True).count()  # noqa
        context = {
            'candidates': candidates,
            'total_votes_cast': total_votes_cast,
            'current_election': current_election,
        }
        return render(request, self.template, context)
