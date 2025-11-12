from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('accounts/profile/update/', views.update_profile, name='update_profile'),
    path('cats/add/', views.add_cat, name='add_cat'),
    path('cats/', views.ListCats, name='list_cats'),
    path('cat/<int:cat_id>/', views.cat_detail, name='cat_details'),
]