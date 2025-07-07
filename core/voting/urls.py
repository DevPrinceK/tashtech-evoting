from django.urls import path
from . import views as views


app_name = 'voting'

# generals
urlpatterns = [
    path('instructions/', views.InstructionsView.as_view(), name='instructions'),
    path('castvote/', views.CastVoteView.as_view(), name='cast_vote'),  # noqa
    path('votecompleted/', views.VoteCompletedView.as_view(), name='vote_completed'),  # noqa
    path('alreadyvoted/', views.AlreadyVotedView.as_view(), name='already_voted'),  # noqa
]