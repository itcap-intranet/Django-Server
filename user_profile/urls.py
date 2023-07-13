from django.urls import path
from .views import profile
from user_profile.crud.user_profile_crud import profile_update
from django.contrib.auth import views as auth_views

app_name = 'user_profile'

urlpatterns = [
    path('view/', profile, name='profile'),
    path('update/', profile_update, name='profile-update'),

]