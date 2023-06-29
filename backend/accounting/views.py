from django.shortcuts import render, get_object_or_404

from .models import Ticket


def view_tickets(request):
    if request.user:
        ticket_item = Ticket.objects.all()
        context = {
            'ticket_item': ticket_item,
            'title': 'Tickets',
        }
    else:
        ticket_item = 'ticket_item'
        context = {
            'ticket_item': ticket_item,
            'title': 'Tickets',
        }
    return render(request, 'accounting/index.html', context=context)
