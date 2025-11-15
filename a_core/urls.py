from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('accounts/profile/update/', views.update_profile, name='update_profile'),
    path('account/<str:user_id>/', views.other_profile_view, name='other_profile'),
    path('cats/add/', views.add_cat, name='add_cat'),
    path('cats/', views.ListCats, name='list_cats'),
    path('cat/<int:cat_id>/', views.cat_detail, name='cat_details'),
    path('cat/<int:cat_id>/request_adoption/', views.request_adoption, name='request_adoption'),
    path('adoption_request/<int:adoption_request_id>/cancel/', views.cancel_adoption_request, name='cancel_adoption_request'),
    path('adoption_request/<int:adoption_request_id>/accept/', views.accept_adoption_request, name='accept_adoption_request'),
]