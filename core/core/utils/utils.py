from django.shortcuts import redirect


def check_already_voted(user):
    '''Checks if voter has already voted'''
    if user.voted_for_all:
        return redirect('voting:already_voted')


def vote_for_all(request):
    '''flags voters who have already voted for all positions'''
    voter = request.user
    # if voter.voted_for_sp and voter.voted_for_gp and voter.voted_for_cob and voter.voted_for_cog and voter.voted_for_sgpb and voter.voted_for_sgpg and voter.voted_for_dhpb and voter.voted_for_dhpg and voter.voted_for_ecpb and voter.voted_for_ecpg and voter.voted_for_lpb and voter.voted_for_lpg and voter.voted_for_csb and voter.voted_for_csg and voter.voted_for_hspb and voter.voted_for_hspg and voter.voted_for_hpb and voter.voted_for_hpg:
    voter.voted_for_all = True
    voter.save()
