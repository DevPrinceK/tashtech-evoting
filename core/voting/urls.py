from django.urls import path
from . import views


app_name = 'voting'

# generals
urlpatterns = [
    path('instructions/', views.InstructionsView.as_view(), name='instructions'),
    path('vote-completed/', views.VoteCompletedView.as_view(), name='vote_completed'),  # noqa
    path('already-voted/', views.AlreadyVotedView.as_view(), name='already_voted'),  # noqa
]

# senior prefects
urlpatterns += [
    path('vote-sp/', views.VoteSPView.as_view(), name='vote_sp'),
    path('vote-gp/', views.VoteGPView.as_view(), name='vote_gp'),
]

# compound overseers
urlpatterns += [
    path('vote-cob/', views.VoteCOBView.as_view(), name='vote_cob'),
    path('vote-cog/', views.VoteCOGView.as_view(), name='vote_cog'),
]

# sports & games prefects
urlpatterns += [
    path('vote-sgpb/', views.VoteSGPBView.as_view(), name='vote_sgpb'),
    path('vote-sgpg/', views.VoteSGPGView.as_view(), name='vote_sgpg'),
]

# dining hall prefects
urlpatterns += [
    path('vote-dhpb/', views.VoteDHPBView.as_view(), name='vote_dhpb'),
    path('vote-dhpg/', views.VoteDHPGView.as_view(), name='vote_dhpg'),
]

# entertainment prefects
urlpatterns += [
    path('vote-ecpb/', views.VoteECPBView.as_view(), name='vote_ecpb'),
    path('vote-ecpg/', views.VoteECPGView.as_view(), name='vote_ecpg'),
]

# library prefects
urlpatterns += [
    path('vote-lpb/', views.VoteLPBView.as_view(), name='vote_lpb'),
    path('vote-lpg/', views.VoteLPGView.as_view(), name='vote_lpg'),
]

# chapel steward prefects
urlpatterns += [
    path('vote-csb/', views.VoteCSBView.as_view(), name='vote_csb'),
    path('vote-csg/', views.VoteCSGView.as_view(), name='vote_csg'),
]

# preps prefects
urlpatterns += [
    path('vote-ppb/', views.VotePPBView.as_view(), name='vote_ppb'),
    path('vote-ppg/', views.VotePPGView.as_view(), name='vote_ppg'),
]

# health and sanitation prefects
urlpatterns += [
    path('vote-hspb/', views.VoteHSPBView.as_view(), name='vote_hspb'),
    path('vote-hspg/', views.VoteHSPGView.as_view(), name='vote_hspg'),
]

# house prefects
urlpatterns += [
    path('vote-hpb/', views.VoteHPBView.as_view(), name='vote_hpb'),
    path('vote-hpg/', views.VoteHPGView.as_view(), name='vote_hpg'),
]
