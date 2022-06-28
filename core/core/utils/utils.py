from django.shortcuts import render, redirect


def check_already_voted(request):
    '''Checks if voter has already voted'''
    if request.user.voted_for_all:
        return redirect('voting:already_voted')
    pass

