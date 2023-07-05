from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib import messages

from backend.models import Candidate, Position
from core.utils.decorators import MustLogin
from core.utils.constants import PositionName, Sex
from core.utils.utils import check_already_voted, vote_for_all


class InstructionsView(View):
    '''Entry point of election'''
    template = 'voting/instructions.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        # if request.user.voted_for_all:
        # return redirect('voting:already_voted')
        if request.user.voted_for_all:
            return redirect('voting:already_voted')
        return render(request, self.template, {})


class VoteSPView(View):
    '''Implements voting for SENIOR BOYS PREFECTS'''
    template = 'voting/vote.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        if request.user.voted_for_all:
            # check if voter has already voted
            return redirect('voting:already_voted')
        candidates = Candidate.objects.filter(position__name=PositionName.SP.value).order_by('ballot_number')  # noqa
        # flag for yes or no vote
        if candidates.count() == 1:
            acclamation = True
        else:
            acclamation = False
        context = {
            'position': PositionName.SP.value,
            'candidates': candidates,
            'acclamation': acclamation,
        }
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        if request.user.voted_for_all:
            # check if voter has already voted
            return redirect('voting:already_voted')
        # already voted for this portfolio
        if request.user.voted_for_sp:
            messages.success(request, "Access Denied! You've already voted for this portfolio.")  # noqa
            return redirect('voting:vote_gp')
        # acclamation vote
        acclamation = True if request.POST.get('acclamation') is not None else False  # noqa
        no_vote = request.POST.get('no_vote') or None
        if acclamation and no_vote == "NO":
            candidate_id = request.POST.get('candidate_id')
            candidate = Candidate.objects.filter(position__name=PositionName.SP.value, id=candidate_id).first()  # noqa
            if candidate:
                candidate.no_votes_count += 1
                candidate.save()
                request.user.voted_for_sp = True
                request.user.save()
                return redirect('voting:vote_gp')
        # no acclamation
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
        if request.user.voted_for_all:
            return redirect('voting:already_voted')
        candidates = Candidate.objects.filter(position__name=PositionName.GP.value).order_by('ballot_number')  # noqa
        # flag for yes or no vote
        if candidates.count() == 1:
            acclamation = True
        else:
            acclamation = False
        context = {
            'position': PositionName.GP.value,
            'candidates': candidates,
            'acclamation': acclamation,
        }
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        if request.user.voted_for_all:
            # check if voter has already voted
            return redirect('voting:already_voted')
        # already voted for this portfolio
        if request.user.voted_for_gp:
            messages.success(request, "Access Denied! You've already voted for this portfolio.")  # noqa
            return redirect('voting:vote_cob')
        # acclamation vote
        acclamation = True if request.POST.get('acclamation') is not None else False  # noqa
        no_vote = request.POST.get('no_vote') or None
        if acclamation and no_vote == "NO":
            candidate_id = request.POST.get('candidate_id')
            candidate = Candidate.objects.filter(position__name=PositionName.GP.value, id=candidate_id).first()  # noqa
            if candidate:
                candidate.no_votes_count += 1
                candidate.save()
                request.user.voted_for_gp = True
                request.user.save()
                return redirect('voting:vote_cob')
        # no acclamation
        candidate_id = request.POST.get('candidate_id')
        candidate = Candidate.objects.filter(position__name=PositionName.GP.value, id=candidate_id).first()  # noqa
        # vote
        candidate.vote_count += 1
        candidate.save()
        request.user.voted_for_gp = True
        request.user.save()
        messages.success(request, 'Vote Successful, Proceed to next portfolio.')  # noqa
        return redirect('voting:vote_cob')


class VoteCOBView(View):
    '''Implements voting for COMPOUND OVERSEER - BOYS'''
    template = 'voting/vote.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        if request.user.voted_for_all:
            return redirect('voting:already_voted')
        candidates = Candidate.objects.filter(position__name=PositionName.COB.value).order_by('ballot_number')  # noqa
        # flag for yes or no vote
        if candidates.count() == 1:
            acclamation = True
        else:
            acclamation = False
        context = {
            'position': PositionName.COB.value,
            'candidates': candidates,
            'acclamation': acclamation,
        }
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        if request.user.voted_for_all:
            # check if voter has already voted
            return redirect('voting:already_voted')
        # already voted for this portfolio
        if request.user.voted_for_cob:
            messages.success(request, "Access Denied! You've already voted for this portfolio.")  # noqa
            return redirect('voting:vote_cog')
        # acclamation vote
        acclamation = True if request.POST.get('acclamation') is not None else False  # noqa
        no_vote = request.POST.get('no_vote') or None
        if acclamation and no_vote == "NO":
            candidate_id = request.POST.get('candidate_id')
            candidate = Candidate.objects.filter(position__name=PositionName.COB.value, id=candidate_id).first()  # noqa
            if candidate:
                candidate.no_votes_count += 1
                candidate.save()
                request.user.voted_for_cob = True
                request.user.save()
                return redirect('voting:vote_cog')
        # no acclamation
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
        if request.user.voted_for_all:
            return redirect('voting:already_voted')
        candidates = Candidate.objects.filter(position__name=PositionName.COG.value).order_by('ballot_number')  # noqa
        # flag for yes or no vote
        if candidates.count() == 1:
            acclamation = True
        else:
            acclamation = False
        context = {
            'position': PositionName.COG.value,
            'candidates': candidates,
            'acclamation': acclamation,
        }
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        if request.user.voted_for_all:
            # check if voter has already voted
            return redirect('voting:already_voted')
        # already voted for this portfolio
        if request.user.voted_for_cog:
            messages.success(request, "Access Denied! You've already voted for this portfolio.")  # noqa
            return redirect('voting:vote_sgpb')
        # acclamation vote
        acclamation = True if request.POST.get(
            'acclamation') is not None else False  #
        no_vote = request.POST.get('no_vote') or None
        if acclamation and no_vote == "NO":
            candidate_id = request.POST.get('candidate_id')
            candidate = Candidate.objects.filter(position__name=PositionName.COG.value, id=candidate_id).first()  # noqa
            if candidate:
                candidate.no_votes_count += 1
                candidate.save()
                request.user.voted_for_cog = True
                request.user.save()
                return redirect('voting:vote_sgpb')
        # no acclamation
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
        if request.user.voted_for_all:
            return redirect('voting:already_voted')
        candidates = Candidate.objects.filter(position__name=PositionName.SGPB.value).order_by('ballot_number')  # noqa
        # flag for yes or no vote
        if candidates.count() == 1:
            acclamation = True
        else:
            acclamation = False
        context = {
            'position': PositionName.SGPB.value,
            'candidates': candidates,
            'acclamation': acclamation,
        }
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        if request.user.voted_for_all:
            # check if voter has already voted
            return redirect('voting:already_voted')
        # already voted for this portfolio
        if request.user.voted_for_sgpb:
            messages.success(request, "Access Denied! You've already voted for this portfolio.")  # noqa
            return redirect('voting:vote_sgpg')
        # acclamation vote
        acclamation = True if request.POST.get('acclamation') is not None else False  # noqa
        no_vote = request.POST.get('no_vote') or None
        if acclamation and no_vote == "NO":
            candidate_id = request.POST.get('candidate_id')
            candidate = Candidate.objects.filter(position__name=PositionName.SGPB.value, id=candidate_id).first()  # noqa
            if candidate:
                candidate.no_votes_count += 1
                candidate.save()
                request.user.voted_for_sgpb = True
                request.user.save()
                return redirect('voting:vote_sgpg')
        # no acclamation
        candidate_id = request.POST.get('candidate_id')
        candidate = Candidate.objects.filter(position__name=PositionName.SGPB.value, id=candidate_id).first()  # noqa
        # vote
        candidate.vote_count += 1
        candidate.save()
        request.user.voted_for_sgpb = True
        request.user.save()
        messages.success(request, 'Vote Successful, Proceed to next portfolio.')  # noqa
        return redirect('voting:vote_sgpg')


class VoteSGPGView(View):
    '''Implements voting for SPORTS AND GAMES PREF - GIRLS'''
    template = 'voting/vote.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        if request.user.voted_for_all:
            return redirect('voting:already_voted')
        candidates = Candidate.objects.filter(position__name=PositionName.SGPG.value).order_by('ballot_number')  # noqa
        # flag for yes or no vote
        if candidates.count() == 1:
            acclamation = True
        else:
            acclamation = False
        context = {
            'position': PositionName.SGPG.value,
            'candidates': candidates,
            'acclamation': acclamation,
        }
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        if request.user.voted_for_all:
            # check if voter has already voted
            return redirect('voting:already_voted')
        # already voted for this portfolio
        if request.user.voted_for_sgpg:
            messages.success(request, "Access Denied! You've already voted for this portfolio.")  # noqa
            return redirect('voting:vote_dhpb')
        # acclamation vote
        acclamation = True if request.POST.get('acclamation') is not None else False  # noqa
        no_vote = request.POST.get('no_vote') or None
        if acclamation and no_vote == "NO":
            candidate_id = request.POST.get('candidate_id')
            candidate = Candidate.objects.filter(position__name=PositionName.SGPG.value, id=candidate_id).first()  # noqa
            if candidate:
                candidate.no_votes_count += 1
                candidate.save()
                request.user.voted_for_sgpg = True
                request.user.save()
                return redirect('voting:vote_dhpb')
        # no acclamation
        candidate_id = request.POST.get('candidate_id')
        candidate = Candidate.objects.filter(position__name=PositionName.SGPG.value, id=candidate_id).first()  # noqa
        # vote
        candidate.vote_count += 1
        candidate.save()
        request.user.voted_for_sgpg = True
        request.user.save()
        messages.success(request, 'Vote Successful, Proceed to next portfolio.')  # noqa
        return redirect('voting:vote_dhpb')


class VoteDHPBView(View):
    '''Implements voting for DINING HALL PREFECT - BOYS'''
    template = 'voting/vote.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        if request.user.voted_for_all:
            return redirect('voting:already_voted')
        candidates = Candidate.objects.filter(position__name=PositionName.DHPB.value).order_by('ballot_number')  # noqa
        # flag for yes or no vote
        if candidates.count() == 1:
            acclamation = True
        else:
            acclamation = False
        context = {
            'position': PositionName.DHPB.value,
            'candidates': candidates,
            'acclamation': acclamation,
        }
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        if request.user.voted_for_all:
            # check if voter has already voted
            return redirect('voting:already_voted')
        # already voted for this portfolio
        if request.user.voted_for_dhpb:
            messages.success(request, "Access Denied! You've already voted for this portfolio.")  # noqa
            return redirect('voting:vote_dhpg')
        # acclamation vote
        acclamation = True if request.POST.get('acclamation') is not None else False  # noqa
        no_vote = request.POST.get('no_vote') or None
        if acclamation and no_vote == "NO":
            candidate_id = request.POST.get('candidate_id')
            candidate = Candidate.objects.filter(position__name=PositionName.DHPB.value, id=candidate_id).first()  # noqa
            if candidate:
                candidate.no_votes_count += 1
                candidate.save()
                request.user.voted_for_dhpb = True
                request.user.save()
                return redirect('voting:vote_dhpg')
        # no acclamation
        candidate_id = request.POST.get('candidate_id')
        candidate = Candidate.objects.filter(position__name=PositionName.DHPB.value, id=candidate_id).first()  # noqa
        # vote
        candidate.vote_count += 1
        candidate.save()
        request.user.voted_for_dhpb = True
        request.user.save()
        messages.success(request, 'Vote Successful, Proceed to next portfolio.')  # noqa
        return redirect('voting:vote_dhpg')


class VoteDHPGView(View):
    '''Implements voting for DINING HALL PREFECT - GIRLS'''
    template = 'voting/vote.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        if request.user.voted_for_all:
            return redirect('voting:already_voted')
        candidates = Candidate.objects.filter(position__name=PositionName.DHPG.value).order_by('ballot_number')  # noqa
        # flag for yes or no vote
        if candidates.count() == 1:
            acclamation = True
        else:
            acclamation = False
        context = {
            'position': PositionName.DHPG.value,
            'candidates': candidates,
            'acclamation': acclamation,
        }
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        if request.user.voted_for_all:
            # check if voter has already voted
            return redirect('voting:already_voted')
        # already voted for this portfolio
        if request.user.voted_for_dhpg:
            messages.success(request, "Access Denied! You've already voted for this portfolio.")  # noqa
            return redirect('voting:vote_ecpb')
        # acclamation vote
        acclamation = True if request.POST.get('acclamation') is not None else False  # noqa
        no_vote = request.POST.get('no_vote') or None
        if acclamation and no_vote == "NO":
            candidate_id = request.POST.get('candidate_id')
            candidate = Candidate.objects.filter(position__name=PositionName.DHPG.value, id=candidate_id).first()  # noqa
            if candidate:
                candidate.no_votes_count += 1
                candidate.save()
                request.user.voted_for_dhpg = True
                request.user.save()
                return redirect('voting:vote_ecpb')
        # no acclamation
        candidate_id = request.POST.get('candidate_id')
        candidate = Candidate.objects.filter(position__name=PositionName.DHPG.value, id=candidate_id).first()  # noqa
        # vote
        candidate.vote_count += 1
        candidate.save()
        request.user.voted_for_dhpg = True
        request.user.save()
        messages.success(request, 'Vote Successful, Proceed to next portfolio.')  # noqa
        return redirect('voting:vote_ecpb')


class VoteECPBView(View):
    '''Implements voting for ENTERTAINMENT AND CULTURE PREF - BOYS'''
    template = 'voting/vote.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        if request.user.voted_for_all:
            return redirect('voting:already_voted')
        candidates = Candidate.objects.filter(position__name=PositionName.ECPB.value).order_by('ballot_number')  # noqa
        # flag for yes or no vote
        if candidates.count() == 1:
            acclamation = True
        else:
            acclamation = False
        context = {
            'position': PositionName.ECPB.value,
            'candidates': candidates,
            'acclamation': acclamation,
        }
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        if request.user.voted_for_all:
            # check if voter has already voted
            return redirect('voting:already_voted')
        # already voted for this portfolio
        if request.user.voted_for_ecpb:
            messages.success(request, "Access Denied! You've already voted for this portfolio.")  # noqa
            return redirect('voting:vote_ecpg')
        # acclamation vote
        acclamation = True if request.POST.get('acclamation') is not None else False  # noqa
        no_vote = request.POST.get('no_vote') or None
        if acclamation and no_vote == "NO":
            candidate_id = request.POST.get('candidate_id')
            candidate = Candidate.objects.filter(position__name=PositionName.ECPB.value, id=candidate_id).first()  # noqa
            if candidate:
                candidate.no_votes_count += 1
                candidate.save()
                request.user.voted_for_ecpb = True
                request.user.save()
                return redirect('voting:vote_ecpg')
        # no acclamation
        candidate_id = request.POST.get('candidate_id')
        candidate = Candidate.objects.filter(position__name=PositionName.ECPB.value, id=candidate_id).first()  # noqa
        # vote
        candidate.vote_count += 1
        candidate.save()
        request.user.voted_for_ecpb = True
        request.user.save()
        messages.success(request, 'Vote Successful, Proceed to next portfolio.')  # noqa
        return redirect('voting:vote_ecpg')


class VoteECPGView(View):
    '''Implements voting for ENTERTAINMENT AND CULTURE PREF - GIRLS'''
    template = 'voting/vote.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        if request.user.voted_for_all:
            return redirect('voting:already_voted')
        candidates = Candidate.objects.filter(position__name=PositionName.ECPG.value).order_by('ballot_number')  # noqa
        # flag for yes or no vote
        if candidates.count() == 1:
            acclamation = True
        else:
            acclamation = False
        context = {
            'position': PositionName.ECPG.value,
            'candidates': candidates,
            'acclamation': acclamation,
        }
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        if request.user.voted_for_all:
            # check if voter has already voted
            return redirect('voting:already_voted')
        # already voted for this portfolio
        if request.user.voted_for_ecpg:
            messages.success(request, "Access Denied! You've already voted for this portfolio.")  # noqa
            return redirect('voting:vote_lpb')
        # acclamation vote
        acclamation = True if request.POST.get('acclamation') is not None else False  # noqa
        no_vote = request.POST.get('no_vote') or None
        if acclamation and no_vote == "NO":
            candidate_id = request.POST.get('candidate_id')
            candidate = Candidate.objects.filter(position__name=PositionName.ECPG.value, id=candidate_id).first()  # noqa
            if candidate:
                candidate.no_votes_count += 1
                candidate.save()
                request.user.voted_for_ecpg = True
                request.user.save()
                return redirect('voting:vote_lpb')
        # no acclamation
        candidate_id = request.POST.get('candidate_id')
        candidate = Candidate.objects.filter(position__name=PositionName.ECPG.value, id=candidate_id).first()  # noqa
        # vote
        candidate.vote_count += 1
        candidate.save()
        request.user.voted_for_ecpg = True
        request.user.save()
        messages.success(request, 'Vote Successful, Proceed to next portfolio.')  # noqa
        return redirect('voting:vote_lpb')


class VoteLPBView(View):
    '''Implements voting for PREP and LIBRARY PREFECT - BOYS'''
    template = 'voting/vote.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        if request.user.voted_for_all:
            return redirect('voting:already_voted')
        candidates = Candidate.objects.filter(position__name=PositionName.PLPB.value).order_by('ballot_number')  # noqa
        # flag for yes or no vote
        if candidates.count() == 1:
            acclamation = True
        else:
            acclamation = False
        context = {
            'position': PositionName.PLPB.value,
            'candidates': candidates,
            'acclamation': acclamation,
        }
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        if request.user.voted_for_all:
            # check if voter has already voted
            return redirect('voting:already_voted')
        # already voted for this portfolio
        if request.user.voted_for_lpb:
            messages.success(request, "Access Denied! You've already voted for this portfolio.")  # noqa
            return redirect('voting:vote_lpg')
        # acclamation vote
        acclamation = True if request.POST.get('acclamation') is not None else False  # noqa
        no_vote = request.POST.get('no_vote') or None
        if acclamation and no_vote == "NO":
            candidate_id = request.POST.get('candidate_id')
            candidate = Candidate.objects.filter(position__name=PositionName.PLPB.value, id=candidate_id).first()  # noqa
            if candidate:
                candidate.no_votes_count += 1
                candidate.save()
                request.user.voted_for_lpb = True
                request.user.save()
                return redirect('voting:vote_lpg')
        # no acclamation
        candidate_id = request.POST.get('candidate_id')
        candidate = Candidate.objects.filter(position__name=PositionName.PLPB.value, id=candidate_id).first()  # noqa
        # vote
        candidate.vote_count += 1
        candidate.save()
        request.user.voted_for_lpb = True
        request.user.save()
        messages.success(request, 'Vote Successful, Proceed to next portfolio.')  # noqa
        return redirect('voting:vote_lpg')


class VoteLPGView(View):
    '''Implements voting for LIBRARY and PREP PREFECT - GIRLS'''
    template = 'voting/vote.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        if request.user.voted_for_all:
            return redirect('voting:already_voted')
        candidates = Candidate.objects.filter(position__name=PositionName.PLPG.value).order_by('ballot_number')  # noqa
        # flag for yes or no vote
        if candidates.count() == 1:
            acclamation = True
        else:
            acclamation = False
        context = {
            'position': PositionName.PLPG.value,
            'candidates': candidates,
            'acclamation': acclamation,
        }
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        if request.user.voted_for_all:
            # check if voter has already voted
            return redirect('voting:already_voted')
        # already voted for this portfolio
        if request.user.voted_for_lpg:
            messages.success(request, "Access Denied! You've already voted for this portfolio.")  # noqa
            return redirect('voting:vote_csb')
        # acclamation vote
        acclamation = True if request.POST.get('acclamation') is not None else False  # noqa
        no_vote = request.POST.get('no_vote') or None
        if acclamation and no_vote == "NO":
            candidate_id = request.POST.get('candidate_id')
            candidate = Candidate.objects.filter(position__name=PositionName.PLPG.value, id=candidate_id).first()  # noqa
            if candidate:
                candidate.no_votes_count += 1
                candidate.save()
                request.user.voted_for_lpg = True
                request.user.save()
                return redirect('voting:vote_csb')
        # no acclamation
        candidate_id = request.POST.get('candidate_id')
        candidate = Candidate.objects.filter(position__name=PositionName.PLPG.value, id=candidate_id).first()  # noqa
        # vote
        candidate.vote_count += 1
        candidate.save()
        request.user.voted_for_lpg = True
        request.user.save()
        messages.success(request, 'Vote Successful, Proceed to next portfolio.')  # noqa
        return redirect('voting:vote_csb')


class VoteCSBView(View):
    '''Implements voting for CHAPEL STEWARD - BOYS'''
    template = 'voting/vote.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        if request.user.voted_for_all:
            return redirect('voting:already_voted')
        candidates = Candidate.objects.filter(position__name=PositionName.CSB.value).order_by('ballot_number')  # noqa
        # flag for yes or no vote
        if candidates.count() == 1:
            acclamation = True
        else:
            acclamation = False
        context = {
            'position': PositionName.CSB.value,
            'candidates': candidates,
            'acclamation': acclamation,
        }
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        if request.user.voted_for_all:
            # check if voter has already voted
            return redirect('voting:already_voted')
        # already voted for this portfolio
        if request.user.voted_for_csb:
            messages.success(request, "Access Denied! You've already voted for this portfolio.")  # noqa
            return redirect('voting:vote_csg')
        # acclamation vote
        acclamation = True if request.POST.get('acclamation') is not None else False  # noqa
        no_vote = request.POST.get('no_vote') or None
        if acclamation and no_vote == "NO":
            candidate_id = request.POST.get('candidate_id')
            candidate = Candidate.objects.filter(position__name=PositionName.CSB.value, id=candidate_id).first()  # noqa
            if candidate:
                candidate.no_votes_count += 1
                candidate.save()
                request.user.voted_for_csb = True
                request.user.save()
                return redirect('voting:vote_csg')
        # no acclamation
        candidate_id = request.POST.get('candidate_id')
        candidate = Candidate.objects.filter(position__name=PositionName.CSB.value, id=candidate_id).first()  # noqa
        # vote
        candidate.vote_count += 1
        candidate.save()
        request.user.voted_for_csb = True
        request.user.save()
        messages.success(request, 'Vote Successful, Proceed to next portfolio.')  # noqa
        return redirect('voting:vote_csg')


class VoteCSGView(View):
    '''Implements voting for CHAPEL STEWARD - GIRLS'''
    template = 'voting/vote.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        if request.user.voted_for_all:
            return redirect('voting:already_voted')
        candidates = Candidate.objects.filter(position__name=PositionName.CSG.value).order_by('ballot_number')  # noqa
        # flag for yes or no vote
        if candidates.count() == 1:
            acclamation = True
        else:
            acclamation = False
        context = {
            'position': PositionName.CSG.value,
            'candidates': candidates,
            'acclamation': acclamation,
        }
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        if request.user.voted_for_all:
            # check if voter has already voted
            return redirect('voting:already_voted')
        # already voted for this portfolio
        if request.user.voted_for_csg:
            messages.success(request, "Access Denied! You've already voted for this portfolio.")  # noqa
            return redirect('voting:vote_hspb')
        # acclamation vote
        acclamation = True if request.POST.get('acclamation') is not None else False  # noqa
        no_vote = request.POST.get('no_vote') or None
        if acclamation and no_vote == "NO":
            candidate_id = request.POST.get('candidate_id')
            candidate = Candidate.objects.filter(position__name=PositionName.CSG.value, id=candidate_id).first()  # noqa
            if candidate:
                candidate.no_votes_count += 1
                candidate.save()
                request.user.voted_for_csg = True
                request.user.save()
                return redirect('voting:vote_hspb')
        # no acclamation
        candidate_id = request.POST.get('candidate_id')
        candidate = Candidate.objects.filter(position__name=PositionName.CSG.value, id=candidate_id).first()  # noqa
        # vote
        candidate.vote_count += 1
        candidate.save()
        request.user.voted_for_csg = True
        request.user.save()
        messages.success(request, 'Vote Successful, Proceed to next portfolio.')  # noqa
        return redirect('voting:vote_hspb')


class VoteHSPBView(View):
    '''Implements voting for HEALTH SANITATION and ATTIRE PREFECT - BOYS'''
    template = 'voting/vote.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        if request.user.voted_for_all:
            return redirect('voting:already_voted')
        candidates = Candidate.objects.filter(position__name=PositionName.HSPB.value).order_by('ballot_number')  # noqa
        # flag for yes or no vote
        if candidates.count() == 1:
            acclamation = True
        else:
            acclamation = False
        context = {
            'position': PositionName.HSPB.value,
            'candidates': candidates,
            'acclamation': acclamation,
        }
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        if request.user.voted_for_all:
            # check if voter has already voted
            return redirect('voting:already_voted')
        # already voted for this portfolio
        if request.user.voted_for_hspb:
            messages.success(request, "Access Denied! You've already voted for this portfolio.")  # noqa
            return redirect('voting:vote_hspg')
        # acclamation vote
        acclamation = True if request.POST.get('acclamation') is not None else False  # noqa
        no_vote = request.POST.get('no_vote') or None
        if acclamation and no_vote == "NO":
            candidate_id = request.POST.get('candidate_id')
            candidate = Candidate.objects.filter(
                position__name=PositionName.HSPB.value, id=candidate_id).first()
            if candidate:
                candidate.no_votes_count += 1
                candidate.save()
                request.user.voted_for_hspb = True
                request.user.save()
                return redirect('voting:vote_hspg')
        # no acclamation
        candidate_id = request.POST.get('candidate_id')
        candidate = Candidate.objects.filter(position__name=PositionName.HSPB.value, id=candidate_id).first()  # noqa
        # vote
        candidate.vote_count += 1
        candidate.save()
        request.user.voted_for_hspb = True
        request.user.save()
        messages.success(request, 'Vote Successful, Proceed to next portfolio.')  # noqa
        return redirect('voting:vote_hspg')


class VoteHSPGView(View):
    '''Implements voting for HEALTH SANITATION and ATTIRE PREFECT - GIRLS'''
    template = 'voting/vote.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        if request.user.voted_for_all:
            return redirect('voting:already_voted')
        candidates = Candidate.objects.filter(position__name=PositionName.HSPG.value).order_by('ballot_number')  # noqa
        # flag for yes or no vote
        if candidates.count() == 1:
            acclamation = True
        else:
            acclamation = False
        context = {
            'position': PositionName.HSPG.value,
            'candidates': candidates,
            'acclamation': acclamation,
        }
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        if request.user.voted_for_all:
            # check if voter has already voted
            return redirect('voting:already_voted')
        # already voted for this portfolio
        if request.user.voted_for_hspg:
            messages.success(request, "Access Denied! You've already voted for this portfolio.")  # noqa
            return redirect('voting:vote_hpb')
        # acclamation vote
        acclamation = True if request.POST.get('acclamation') is not None else False  # noqa
        no_vote = request.POST.get('no_vote') or None
        if acclamation and no_vote == "NO":
            candidate_id = request.POST.get('candidate_id')
            candidate = Candidate.objects.filter(position__name=PositionName.HSPG.value, id=candidate_id).first()  # noqa
            if candidate:
                candidate.no_votes_count += 1
                candidate.save()
                request.user.voted_for_hspg = True
                request.user.save()
                return redirect('voting:vote_hpb')
        # no acclamation

        candidate_id = request.POST.get('candidate_id')
        candidate = Candidate.objects.filter(position__name=PositionName.HSPG.value, id=candidate_id).first()  # noqa
        # vote
        candidate.vote_count += 1
        candidate.save()
        request.user.voted_for_hspg = True
        request.user.save()
        messages.success(request, 'Vote Successful, Proceed to next portfolio.')  # noqa
        return redirect('voting:vote_hpb')


class VoteHPBView(View):
    '''Implements voting for HOUSE PREFECT - BOYS'''
    template = 'voting/vote.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        if request.user.voted_for_all:
            return redirect('voting:already_voted')
        candidates = Candidate.objects.filter(position__name=PositionName.HPB.value, house=request.user.house, sex=Sex.M.value).order_by('ballot_number')  # noqa
        # flag for yes or no vote
        if candidates.count() == 1:
            acclamation = True
        else:
            acclamation = False
        context = {
            'position': PositionName.HPB.value,
            'candidates': candidates,
            'acclamation': acclamation,
        }
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        if request.user.voted_for_all:
            # check if voter has already voted
            return redirect('voting:already_voted')
        # already voted for this portfolio
        if request.user.voted_for_hpb:
            messages.success(request, "Access Denied! You've already voted for this portfolio.")  # noqa
            return redirect('voting:vote_hpg')
        # acclamation vote
        acclamation = True if request.POST.get('acclamation') is not None else False  # noqa
        no_vote = request.POST.get('no_vote') or None
        if acclamation and no_vote == "NO":
            candidate_id = request.POST.get('candidate_id')
            candidate = Candidate.objects.filter(position__name=PositionName.HPB.value, id=candidate_id).first()  # noqa
            if candidate:
                candidate.no_votes_count += 1
                candidate.save()
                request.user.voted_for_hpb = True
                request.user.save()
                return redirect('voting:vote_hpg')
        # no acclamation
        candidate_id = request.POST.get('candidate_id')
        candidate = Candidate.objects.filter(
            position__name=PositionName.HPB.value, house=request.user.house, sex=Sex.M.value, id=candidate_id).first()
        # vote
        candidate.vote_count += 1
        candidate.save()
        request.user.voted_for_hpb = True
        request.user.save()
        messages.success(request, 'Vote Successful, Proceed to next portfolio.')  # noqa
        return redirect('voting:vote_hpg')


class VoteHPGView(View):
    '''Implements voting for HOUSE PREFECT - GIRLS'''
    template = 'voting/vote.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        if request.user.voted_for_all:
            return redirect('voting:already_voted')
        candidates = Candidate.objects.filter(position__name=PositionName.HPG.value, house=request.user.house, sex=Sex.F.value).order_by('ballot_number')  # noqa
        # flag for yes or no vote
        if candidates.count() == 1:
            acclamation = True
        else:
            acclamation = False
        context = {
            'position': PositionName.HPG.value,
            'candidates': candidates,
            'acclamation': acclamation,
        }
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        if request.user.voted_for_all:
            # check if voter has already voted
            return redirect('voting:already_voted')
        # already voted for this portfolio
        if request.user.voted_for_hpg:
            messages.success(request, "Access Denied! You've already voted for this portfolio.")  # noqa
            return redirect('voting:vote_completed')
        # acclamation vote
        acclamation = True if request.POST.get('acclamation') is not None else False  # noqa
        no_vote = request.POST.get('no_vote') or None
        if acclamation and no_vote == "NO":
            candidate_id = request.POST.get('candidate_id')
            candidate = Candidate.objects.filter(position__name=PositionName.HPG.value, id=candidate_id).first()  # noqa
            if candidate:
                candidate.no_votes_count += 1
                candidate.save()
                request.user.voted_for_hpg = True
                vote_for_all(request)
                request.user.save()
                return redirect('voting:vote_completed')
        # no acclamation
        candidate_id = request.POST.get('candidate_id')
        candidate = Candidate.objects.filter(
            position__name=PositionName.HPG.value, house=request.user.house, sex=Sex.F.value, id=candidate_id).first()
        # vote
        candidate.vote_count += 1
        candidate.save()
        request.user.voted_for_hpg = True
        if request.user.status == "BOARDING":
            vote_for_all(request)
            request.user.save()
            messages.success(request, 'Vote Successful, Proceed to next portfolio.')  # noqa
            return redirect('voting:vote_completed')
        else:
            messages.success(request, 'Vote Successful, Proceed to next portfolio.')  # noqa
            return redirect('voting:vote_dscb')


class VoteDSCBView(View):
    '''Implements voting for DAY STUDENTS COORDINATOR - BOY'''
    template = 'voting/vote.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        if request.user.voted_for_all or request.user.status == "BOARDING":
            return redirect('voting:already_voted')
        candidates = Candidate.objects.filter(position__name=PositionName.DSCB.value, sex=Sex.M.value).order_by('ballot_number')  # noqa
        # flag for yes or no vote
        if candidates.count() == 1:
            acclamation = True
        else:
            acclamation = False
        context = {
            'position': PositionName.DSCB.value,
            'candidates': candidates,
            'acclamation': acclamation,
        }
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        if request.user.voted_for_all:
            # check if voter has already voted
            return redirect('voting:already_voted')
        # already voted for this portfolio
        if request.user.voted_for_day_std_coordinator:
            messages.success(request, "Access Denied! You've already voted for this portfolio.")  # noqa
            return redirect('voting:vote_dscg')
        # acclamation vote
        acclamation = True if request.POST.get('acclamation') is not None else False  # noqa
        no_vote = request.POST.get('no_vote') or None
        if acclamation and no_vote == "NO":
            candidate_id = request.POST.get('candidate_id')
            candidate = Candidate.objects.filter(position__name=PositionName.DSCB.value, id=candidate_id).first()  # noqa
            if candidate:
                candidate.no_votes_count += 1
                candidate.save()
                request.user.voted_for_day_std_coordinator = True
                vote_for_all(request)
                request.user.save()
                return redirect('voting:vote_completed')
        # no acclamation
        candidate_id = request.POST.get('candidate_id')
        candidate = Candidate.objects.filter(
            position__name=PositionName.DSCB.value, sex=Sex.M.value, id=candidate_id).first()
        # vote
        candidate.vote_count += 1
        candidate.save()
        request.user.voted_for_hpg = True
        if request.user.status == "BOARDING":
            vote_for_all(request)
            request.user.save()
            messages.success(request, 'Vote Successful, Proceed to next portfolio.')  # noqa
            return redirect('voting:vote_completed')
        else:
            messages.success(request, 'Vote Successful, Proceed to next portfolio.')  # noqa
            return redirect('voting:vote_dscg')


class VoteDSCGView(View):
    '''Implements voting for DAY STUDENTS COORDINATOR - GIRLS'''
    template = 'voting/vote.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        if request.user.voted_for_all or request.user.status == "BOARDING":
            return redirect('voting:already_voted')
        candidates = Candidate.objects.filter(position__name=PositionName.DSCG.value, sex=Sex.F.value).order_by('ballot_number')  # noqa
        # flag for yes or no vote
        if candidates.count() == 1:
            acclamation = True
        else:
            acclamation = False
        context = {
            'position': PositionName.DSCG.value,
            'candidates': candidates,
            'acclamation': acclamation,
        }
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        if request.user.voted_for_all:
            # check if voter has already voted
            return redirect('voting:already_voted')
        # already voted for this portfolio
        if request.user.voted_for_day_std_coordinator:
            messages.success(request, "Access Denied! You've already voted for this portfolio.")  # noqa
            return redirect('voting:already_voted')
        # acclamation vote
        acclamation = True if request.POST.get('acclamation') is not None else False  # noqa
        no_vote = request.POST.get('no_vote') or None
        print(f"ACCLAMATION: {acclamation}")
        print(f"NO VOTE: {no_vote}")
        if acclamation and no_vote == "NO":
            candidate_id = request.POST.get('candidate_id')
            candidate = Candidate.objects.filter(position__name=PositionName.DSCG.value, id=candidate_id).first()  # noqa
            if candidate:
                candidate.no_votes_count += 1
                candidate.save()
                request.user.voted_for_day_std_coordinator_g = True
                vote_for_all(request)
                request.user.save()
                return redirect('voting:vote_completed')
        # no acclamation
        candidate_id = request.POST.get('candidate_id')
        candidate = Candidate.objects.filter(
            position__name=PositionName.DSCB.value, sex=Sex.F.value, id=candidate_id).first()
        # vote
        candidate.vote_count += 1
        candidate.save()
        request.user.voted_for_hpg = True
        vote_for_all(request)
        request.user.save()
        messages.success(request, 'Vote Successful, Proceed to next portfolio.')  # noqa
        return redirect('voting:vote_completed')


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


class NoVoteView(View):
    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        candidate_id = request.GET.get('candidate_id')
        position_id = request.GET.get('position_id')
        candidate = Candidate.objects.filter(
            id=candidate_id, position__id=position_id).first()
        position = Position.objects.filter(id=position_id).first()
        if candidate:
            candidate.no_votes_count += 1
            candidate.save()
            messages.success(
                request, 'Vote Successful, Proceed to next portfolio.')
            if position.name == PositionName.SP.value:
                request.user.voted_for_sp = True
