from django.urls import path
from .views import add_profile, search_profile

urlpatterns = [
    path('', add_profile),
    path('search/', search_profile)
]