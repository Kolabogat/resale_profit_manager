from django.urls import path

from .views import *

urlpatterns = [
    path('', view_tickets, name='home'),
    path('about/', view_about, name='about'),
]
