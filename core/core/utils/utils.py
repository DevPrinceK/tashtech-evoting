from django.db import models

from backend.models import Position


def get_next_position(request):
    '''
    returns the next position that the voter is
    elegible to vote for.
    '''
    voter = request.user
    positions = Position.objects.annotate(num_candidates=models.Count('candidate')).filter(num_candidates__gt=0).order_by("precedence")
    positions_voted_for = voter.total_votes_cast or 0
    total_positions = positions.count()
    next_postion_indx = positions_voted_for + 1
    is_house_prefect = False
    print(f"Total positions: {total_positions}, "
          f"Positions voted for: {positions_voted_for}, "
          f"Next position index: {next_postion_indx}")
    if next_postion_indx <= total_positions:
        # user can vote for next position
        position_name = positions[next_postion_indx - 1].name
        if position_name.upper().startswith("HOUSE PREFECT"):
            # House Prefect position -- filter candidates based on voter's house
            is_house_prefect = True
        return next_postion_indx, is_house_prefect
    else:
        # user has voted for all positions
        return -999, is_house_prefect


def get_next_position_name(request) -> str:
    '''
    returns the name of the next position that the voter is
    elegible to vote for.
    '''
    next_position_indx = get_next_position(request)
    if next_position_indx == -999:
        return "No more positions to vote for"
    # positions = Position.objects.all().order_by("precedence")
    positions = Position.objects.annotate(num_candidates=models.Count('candidate')).filter(num_candidates__gt=0).order_by("precedence")
    return positions[next_position_indx - 1].name  # adjust for zero-based index