from django.shortcuts import redirect

from backend.models import Position


def get_next_position(request) -> int:
    '''
    returns the next position that the voter is
    elegible to vote for.
    '''
    voter = request.user
    positions = Position.objects.all().order_by("precedence")
    positions_voted_for = voter.total_votes_cast or 0
    total_positions = positions.count()
    next_postion_indx = positions_voted_for + 1
    if next_postion_indx <= total_positions:
        # user can vote for next position
        return next_postion_indx
    else:
        # user has voted for all positions
        return -999


