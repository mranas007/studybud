from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    #  pass a parameter to the url <str:params>| param types: str, int and slug
    path('login/', views.loginView, name='login'),
    path('register/', views.registerView, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('update-user/', views.update_profile, name='update-user'),
]