from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.db import models
from django.contrib import messages

from backend.models import Candidate, Position
from core.utils.decorators import MustLogin
from core.utils.constants import PositionName, Sex
from core.utils.utils import get_next_position


class InstructionsView(View):
    '''Entry point of election'''
    template = 'voting/instructions.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        next_position_indx = get_next_position(request)
        if next_position_indx == -999:
            return redirect('voting:already_voted')
        return render(request, self.template, {})

class CastVoteView(View):
    '''General view for casting votes'''
    template = 'voting/vote.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        next_position_indx, is_house_prefect = get_next_position(request)
        candidates = Candidate.objects.none() 
        if next_position_indx == -999:
            return redirect('voting:already_voted')
        
        if is_house_prefect: # House Prefect position
            # filter candidates based on voter's house
            positions = Position.objects.annotate(num_candidates=models.Count('candidate')).filter(num_candidates__gt=0).order_by("precedence")
            next_position_indx -= 1  # adjust for zero-based index
            position = positions[next_position_indx]
            user_house = request.user.house
            candidates = Candidate.objects.filter(position=position, house__icontains=user_house).order_by('ballot_number')
        else:
            next_position_indx -= 1  # adjust for zero-based index
            positions = Position.objects.annotate(num_candidates=models.Count('candidate')).filter(num_candidates__gt=0).order_by("precedence")
            position = positions[next_position_indx]
            candidates = Candidate.objects.filter(position=position).order_by('ballot_number')
        # flag for yes or no vote
        if candidates.count() == 1:
            acclamation = True
        else:
            acclamation = False
        context = {
            'position': position.name,
            'candidates': candidates,
            'acclamation': acclamation,
        }
        return render(request, self.template, context)
    
    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        next_position_indx, is_house_prefect = get_next_position(request)
        if next_position_indx == -999:
            request.user.already_voted = True
            request.user.save()
            return redirect('voting:already_voted')
        next_position_indx -= 1  # adjust for zero-based index

        # check for acclamation vote | Yes, No
        acclamation = True if request.POST.get('acclamation') is not None else False  # noqa
        candidate_id = request.POST.get('candidate_id')
        no_vote = request.POST.get('no_vote') or None


        if is_house_prefect: # House Prefect position
            # filter candidates based on voter's house
            positions = Position.objects.annotate(num_candidates=models.Count('candidate')).filter(num_candidates__gt=0).order_by("precedence")
            position = positions[next_position_indx]
            user_house = request.user.house
            # candidate = Candidate.objects.filter(position=position, house__icontains=user_house).order_by('ballot_number')
            candidate = Candidate.objects.filter(position=position, id=candidate_id, house__icontains=user_house).first()
        else:
            positions = Position.objects.annotate(num_candidates=models.Count('candidate')).filter(num_candidates__gt=0).order_by("precedence")
            position = positions[next_position_indx]
            candidate = Candidate.objects.filter(position=position, id=candidate_id).first()
        
        if acclamation and no_vote == "NO":
            if candidate:
                candidate.no_votes_count += 1
                candidate.save()
                request.user.total_votes_cast += 1
                request.user.save()
                return redirect('voting:cast_vote')
        # not an acclamation vote
        if not candidate:
            print(f"Invalid candidate selected: {candidate_id} for position {position.name}")  # noqa
            messages.error(request, 'Invalid Candidate Selected')
            return redirect('voting:cast_vote')
        candidate.vote_count += 1
        candidate.save()
        request.user.total_votes_cast += 1
        request.user.save()
        positions_count = positions = Position.objects.annotate(num_candidates=models.Count('candidate')).filter(num_candidates__gt=0).count()
        if request.user.total_votes_cast >= positions_count:
            request.user.already_voted = True
            request.user.save()
            return redirect('voting:vote_completed')
        messages.success(request, 'Vote Successful, Proceed to next portfolio.')  # noqa
        return redirect('voting:cast_vote')

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