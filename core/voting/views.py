from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib import messages

from backend.models import Candidate
from core.utils.decorators import MustLogin
from core.utils.constants import PositionName
from core.utils.utils import check_already_voted


class InstructionsView(View):
    '''Entry point of election'''
    template = 'voting/instructions.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        return render(request, self.template, {})


class VoteSPView(View):
    '''Implements voting for SENIOR BOYS PREFECTS'''
    template = 'voting/vote.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        check_already_voted(request)  # check if voter has already voted
        candidates = Candidate.objects.filter(position__name=PositionName.SP.value).order_by('ballot_number')  # noqa
        context = {
            'position': PositionName.SP.value,
            'candidates': candidates,
        }
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        check_already_voted(request)  # check if voter has already voted
        # already voted for this portfolio
        if request.user.voted_for_sp:
            messages.success(request, "Access Denied! You've already voted for this portfolio.")  # noqa
            return redirect('voting:vote_gp')
        candidate_id = request.POST.get('candidate_id')
        candidate = Candidate.objects.filter(position__name=PositionName.SP.value, id=candidate_id).first()  # noqa
        # vote
        candidate.vote_count += 1
        candidate.save()
        request.user.voted_for_sp = True
        request.user.save()
        messages.success(request, 'Vote Successful, Proceed to next portfolio.')  # noqa
        return redirect('voting:vote_gp')


class VoteGPView(View):
    '''Implements voting for SENIOR GIRLS PREFECTS'''
    template = 'voting/vote.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        check_already_voted(request)
        candidates = Candidate.objects.filter(position__name=PositionName.GP.value).order_by('ballot_number')  # noqa
        context = {
            'position': PositionName.GP.value,
            'candidates': candidates,
        }
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        check_already_voted(request)  # check if voter has already voted
        # already voted for this portfolio
        if request.user.voted_for_gp:
            messages.success(request, "Access Denied! You've already voted for this portfolio.")  # noqa
            return redirect('voting:vote_cob')
        candidate_id = request.POST.get('candidate_id')
        candidate = Candidate.objects.filter(position__name=PositionName.GP.value, id=candidate_id).first()  # noqa
        # vote
        candidate.vote_count += 1
        candidate.save()
        request.user.voted_for_gp = True
        request.user.save()
        messages.success(request, 'Vote Successful, Proceed to next portfolio.')  # noqa
        return redirect('voting:vote_co')


class VoteCOBView(View):
    '''Implements voting for COMPOUND OVERSEER - BOYS'''
    template = 'voting/vote.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        check_already_voted(request)
        candidates = Candidate.objects.filter(position__name=PositionName.COB.value).order_by('ballot_number')  # noqa
        context = {
            'position': PositionName.COB.value,
            'candidates': candidates,
        }
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        check_already_voted(request)  # check if voter has already voted
        # already voted for this portfolio
        if request.user.voted_for_cob:
            messages.success(request, "Access Denied! You've already voted for this portfolio.")  # noqa
            return redirect('voting:vote_cog')
        candidate_id = request.POST.get('candidate_id')
        candidate = Candidate.objects.filter(position__name=PositionName.COB.value, id=candidate_id).first()  # noqa
        # vote
        candidate.vote_count += 1
        candidate.save()
        request.user.voted_for_cob = True
        request.user.save()
        messages.success(request, 'Vote Successful, Proceed to next portfolio.')  # noqa
        return redirect('voting:vote_cog')


class VoteCOGView(View):
    '''Implements voting for COMPOUND OVERSEER - GIRLS'''
    template = 'voting/vote.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        check_already_voted(request)
        candidates = Candidate.objects.filter(position__name=PositionName.COG.value).order_by('ballot_number')  # noqa
        context = {
            'position': PositionName.COG.value,
            'candidates': candidates,
        }
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        check_already_voted(request)  # check if voter has already voted
        # already voted for this portfolio
        if request.user.voted_for_cog:
            messages.success(request, "Access Denied! You've already voted for this portfolio.")  # noqa
            return redirect('voting:vote_sgpb')
        candidate_id = request.POST.get('candidate_id')
        candidate = Candidate.objects.filter(position__name=PositionName.COG.value, id=candidate_id).first()  # noqa
        # vote
        candidate.vote_count += 1
        candidate.save()
        request.user.voted_for_cog = True
        request.user.save()
        messages.success(request, 'Vote Successful, Proceed to next portfolio.')  # noqa
        return redirect('voting:vote_sgpb')


class VoteSGPBView(View):
    '''Implements voting for SPORTS AND GAMES PREF - BOYS'''
    template = 'voting/vote.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        check_already_voted(request)
        candidates = Candidate.objects.filter(position__name=PositionName.SGPB.value).order_by('ballot_number')  # noqa
        context = {
            'position': PositionName.SGPB.value,
            'candidates': candidates,
        }
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        check_already_voted(request)  # check if voter has already voted
        # already voted for this portfolio
        if request.user.voted_for_sgpb:
            messages.success(request, "Access Denied! You've already voted for this portfolio.")  # noqa
            return redirect('voting:vote_sgpg')
        candidate_id = request.POST.get('candidate_id')
        candidate = Candidate.objects.filter(position__name=PositionName.COG.value, id=candidate_id).first()  # noqa
        # vote
        candidate.vote_count += 1
        candidate.save()
        request.user.voted_for_cog = True
        request.user.save()
        messages.success(request, 'Vote Successful, Proceed to next portfolio.')  # noqa
        return redirect('voting:vote_sgpg')


class VoteCompletedView(View):
    '''View to show the vote has been completed'''
    template = 'voting/vote_completed.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        return render(request, self.template, {})


class AlreadyVotedView(View):
    '''View to show the user has already voted'''
    template = 'voting/already_voted.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        return render(request, self.template, {})
