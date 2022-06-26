from django.urls import path
from . import views


app_name = 'voting'
urlpatterns = [
    path('start/', views.StartVotingView.as_view(), name='start_voting'),
    path('sp/', views.VoteSPView.as_view(), name='vote_sp'),
    path('gp/', views.VoteGPView.as_view(), name='vote_gp'),
    path('co/', views.VoteCOView.as_view(), name='vote_co'),
    path('lp/', views.VoteLPView.as_view(), name='vote_lp'),
]
