from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib import messages

from backend.models import Candidate
from core.utils.decorators import MustLogin
from core.utils.constants import PortfolioName


class StartVotingView(View):
    '''Entry point of election'''
    template = 'voting/start_voting.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        return render(request, self.template, {})


class VoteSPView(View):
    '''Implements voting for SENIOR PREFECTS'''
    template = 'voting/vote.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        candidates = Candidate.objects.filter(position__name=PortfolioName.SP.value).order_by('ballot_number')  # noqa
        context = {
            'position': PortfolioName.SP.value,
            'candidates': candidates,
        }
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        # have already completed voting
        if request.user.voted_for_all:
            messages.success(request, "Access Denied! You've already voted!")
            return redirect('voting:already_voted')
        # already voted for this portfolio
        if request.user.voted_for_sp:
            messages.success(request, "Access Denied! You've already voted for this portfolio.")  # noqa
            return redirect('voting:vote_gp')
        candidate_id = request.POST.get('candidate_id')
        candidate = Candidate.objects.filter(position__name=PortfolioName.SP.value, id=candidate_id).first()  # noqa
        # vote
        candidate.vote_count += 1
        candidate.voted_for_sp = True
        candidate.save()
        messages.success(request, 'Vote Successful, Proceed to next portfolio.')  # noqa
        return redirect('voting:vote_gp')


class VoteGPView(View):
    '''Implements voting for GIRLS PREFECTS'''
    template = 'voting/vote.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        candidates = Candidate.objects.filter(position__name=PortfolioName.GP.value).order_by('ballot_number')  # noqa
        context = {
            'position': PortfolioName.GP.value,
            'candidates': candidates,
        }
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        # have already completed voting
        if request.user.voted_for_all:
            messages.success(request, "Access Denied! You've already voted!")
            return redirect('voting:already_voted')
        # already voted for this portfolio
        if request.user.voted_for_gp:
            messages.success(request, "Access Denied! You've already voted for this portfolio.")  # noqa
            return redirect('voting:vote_co')
        candidate_id = request.POST.get('candidate_id')
        candidate = Candidate.objects.filter(position__name=PortfolioName.GP.value, id=candidate_id).first()  # noqa
        # vote
        candidate.vote_count += 1
        candidate.voted_for_gp = True
        candidate.save()
        messages.success(request, 'Vote Successful, Proceed to next portfolio.')  # noqa
        return redirect('voting:vote_co')


class VoteCOView(View):
    '''Implements voting for COMPOUND OVERSEERS'''
    template = 'voting/vote.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        candidates = Candidate.objects.filter(position__name=PortfolioName.CO.value).order_by('ballot_number')  # noqa
        context = {
            'position': PortfolioName.CO.value,
            'candidates': candidates,
        }
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        # have already completed voting
        if request.user.voted_for_all:
            messages.success(request, "Access Denied! You've already voted!")
            return redirect('voting:already_voted')
        # already voted for this portfolio
        if request.user.voted_for_gp:
            messages.success(request, "Access Denied! You've already voted for this portfolio.")  # noqa
            return redirect('voting:vote_lp')
        candidate_id = request.POST.get('candidate_id')
        candidate = Candidate.objects.filter(position__name=PortfolioName.CO.value, id=candidate_id).first()  # noqa
        # vote
        candidate.vote_count += 1
        candidate.voted_for_co = True
        candidate.save()
        messages.success(request, 'Vote Successful, Proceed to next portfolio.')  # noqa
        return redirect('voting:vote_lp')


class VoteLPView(View):
    '''Implements voting for LIBRARY PREFECT'''
    template = 'voting/vote.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        candidates = Candidate.objects.filter(position__name=PortfolioName.LP.value).order_by('ballot_number')  # noqa
        context = {
            'position': PortfolioName.LP.value,
            'candidates': candidates,
        }
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        # have already completed voting
        if request.user.voted_for_all:
            messages.success(request, "Access Denied! You've already voted!")
            return redirect('voting:already_voted')
        # already voted for this portfolio
        if request.user.voted_for_lp:
            messages.success(request, "Access Denied! You've already voted for this portfolio.")  # noqa
            return redirect('voting:vote_completed')
        candidate_id = request.POST.get('candidate_id')
        candidate = Candidate.objects.filter(position__name=PortfolioName.LP.value, id=candidate_id).first()  # noqa
        # vote
        candidate.vote_count += 1
        candidate.voted_for_lp = True
        candidate.voted_for_all = True
        candidate.save()
        messages.success(request, 'Vote Successful, Proceed to next portfolio.')  # noqa
        return redirect('voting:vote_lp')
