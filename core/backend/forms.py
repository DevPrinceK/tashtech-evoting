from django import forms

from .models import Candidate, Election, Position


class CandidateForm(forms.ModelForm):
    '''Facilitates creation and updation of candidates'''
    class Meta:
        model = Candidate
        exclude = ['vote_count', 'position', 'created_at']


class PositionForm(forms.ModelForm):
    '''Facilitates creation and updation of positions'''
    class Meta:
        model = Position
        exclude = ['created_at']


class ElectionForm(forms.ModelForm):
    '''Facilitates creation and updation of elections'''
    class Meta:
        model = Election
        exclude = ['created_at', 'is_active']