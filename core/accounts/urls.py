from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    # path('', views.LandingPageView.as_view(), name='landing_page'),
    path('', views.LoginView.as_view(), name='login'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
