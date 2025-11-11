from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('accounts/profile/update/', views.update_profile, name='update_profile'),
]