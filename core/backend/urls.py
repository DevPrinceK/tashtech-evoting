from unicodedata import name
from django.urls import path
from . import views


app_name = 'backend'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]

# Candidates
urlpatterns += [
    path('candidates/', views.CandidatesListView.as_view(), name='candidates'),
    path('create-update-candiddate/', views.CreateUpdateCandidateView.as_view(), name='create_update_candidate'),  # noqa
    path('delete-candidate/', views.DeleteCandidateView.as_view(), name='delete_candidate')  # noqa
]

# Positions
urlpatterns += [
    path('positions/', views.PositionsView.as_view(), name='positions'),
    path('create-update_position/', views.CreateUpdatePositionView.as_view(), name='create_update_position'),  # noqa
    path('delete-position/', views.DeletePositionView.as_view(), name='delete_position'),  # noqa
]

# Elections
urlpatterns += [
    path('elections/', views.ElectionsView.as_view(), name='elections'),
    path('create-update_election/', views.CreateUpdateElectionView.as_view(), name='create_update_election'),  # noqa
    path('delete-election/', views.DeleteElectionView.as_view(), name='delete_election'),  # noqa
]

# Voters
urlpatterns += [
    path('voters/', views.VotersView.as_view(), name='voters'),
    path('create-update_voter/', views.CreateUpdateVoterView.as_view(), name='create_update_voter'),  # noqa
    path('delete-voter/', views.DeleteVoterView.as_view(), name='delete_voter'),  # noqa
    path('upload-register/', views.UploadVotersFromCSV.as_view(), name='upload_register'),  # noqa
]


# Verification
urlpatterns += [
    path('verification/', views.VerificationView.as_view(), name='verification'),
]

# Results
urlpatterns += [
    path('download-results-csv/', views.DownloadCandidateResultsAsCSVView.as_view(), name='download_results_csv'),  # noqa
]
