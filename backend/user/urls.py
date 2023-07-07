from django.urls import path

from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('password_change/', password_change, name='password_change'),
    path('account_profile/', update_user_data, name='account_profile'),
]
