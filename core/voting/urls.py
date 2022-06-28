from django.urls import path
from . import views


app_name = 'voting'
urlpatterns = [
    path('instructions/', views.InstructionsView.as_view(), name='instructions'),
    path('vote-completed/', views.VoteCompletedView.as_view(), name='vote_completed'),  # noqa
    path('already-voted/', views.AlreadyVotedView.as_view(), name='already_voted'),  # noqa
    path('sp/', views.VoteSPView.as_view(), name='vote_sp'),
    path('gp/', views.VoteGPView.as_view(), name='vote_gp'),
    path('co/', views.VoteCOView.as_view(), name='vote_co'),
    path('lp/', views.VoteLPView.as_view(), name='vote_lp'),
]
