from django.urls import path
from . import views


app_name = 'voting'
urlpatterns = [
    path('vote/sp/', views.VoteSPView.as_view(), name='vote_sp'),
    path('vote/gp/', views.VoteGPView.as_view(), name='vote_gp'),
    path('vote/co/', views.VoteCOView.as_view(), name='vote_co'),
    path('vote/lp/', views.VoteLPView.as_view(), name='vote_lp'),
]
