from django.urls import path

from .views import *

urlpatterns = [
    path('', view_tickets, name='home'),
    path('filter/<str:key>/', view_tickets, name='filter_tickets'),
    path('search/', view_tickets, name='search_tickets'),
    path('add/', add_ticket, name='add_ticket'),
    path('update/<str:id>', update_ticket, name='update_ticket'),
]
