from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('backend/', include('backend.urls')),
    path('vote/', include('voting.urls')),
]
