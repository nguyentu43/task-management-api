from django.urls import path
from .views import add_profile, search_profile, get_my_profile

urlpatterns = [
    path('', add_profile),
    path('me/', get_my_profile),
    path('search/', search_profile)
]