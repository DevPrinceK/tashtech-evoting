from django.urls import path
from . import views


app_name = 'voting'
urlpatterns = [
    path('', views.LandinPageView.as_view(), name='landing_page'),
]
