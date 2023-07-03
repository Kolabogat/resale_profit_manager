from django.urls import path

from .views import *

urlpatterns = [
    path('', view_tickets, name='home'),
    path('<str:key>/', view_filtered_tickets, name='filter_by'),
    path('about/', view_about, name='about'),
    path('add/', add_ticket, name='add_ticket'),
    path('update/<str:id>', update_ticket, name='update_ticket'),
]
