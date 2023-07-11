from django.urls import path

from .views import *

urlpatterns = [
    path('', view_tickets, name='home'),
    path('add/', add_ticket, name='add_ticket'),
    path('update/<int:pk>', update_ticket, name='update_ticket'),
    path('delete/<int:pk>', delete_ticket, name='delete_ticket'),
]
