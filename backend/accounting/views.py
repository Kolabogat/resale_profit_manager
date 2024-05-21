from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from backend.const import TICKETS_FILTER_STATE
from .forms import TicketForm
from .models import Ticket
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from user.models import UserSettings
from .utils import get_filtered_tickets


def view_tickets(request):
    """
    Function that allow user to add waiting or completed ticket.

    Pagination value is taken from individual 'UserSettings' settings.

    Show tickets without any filters. If 'filter_by',
    'order_by' or 'search_filter' are received then check
    the filters in the 'get_filtered_tickets' function.

    Show 'login' template if user not authenticated.
    """
    if request.user.is_authenticated:
        search = request.GET.get('search')
        filter_by = request.GET.get('filter_by')
        order_by = request.GET.get('order_by')
        user_additional = UserSettings.objects.filter(user=request.user).get()
        paginate_by = str(user_additional.paginate_by)

        tickets = get_filtered_tickets(request, search, filter_by, order_by)

        tickets_quantity = tickets.count()
        page = request.GET.get('page', 1)
        paginator = Paginator(tickets, paginate_by)
        try:
            tickets = paginator.page(page)
        except PageNotAnInteger:
            tickets = paginator.page(1)
        except EmptyPage:
            tickets = paginator.page(paginator.num_pages)

        context = {
            'tickets': tickets,
            'tickets_quantity': tickets_quantity,
            'state_filters': TICKETS_FILTER_STATE,
            'user_additional': user_additional,
            'title': 'Tickets',
        }
        if filter_by:
            context['filter_by'] = filter_by
        if order_by:
            context['order_by'] = order_by
        return render(request, 'accounting/index.html', context=context)
    else:
        return redirect('login')


@login_required
def add_ticket(request):
    """
    Function that allow user to add waiting or completed ticket.

    Shows 'add_ticket' template with 'TicketForm' form.
    """
    form = TicketForm(request.POST or None)

    if form.is_valid():
        ticket = form.save(commit=False)
        ticket.user = request.user
        ticket.bought = round(ticket.bought, 2)
        if ticket.sold:
            ticket.sold = round(ticket.sold, 2)
            ticket.profit = round(ticket.sold - ticket.bought, 2)
            ticket.closed = 'True'
        ticket.save()
        messages.success(request, f'Ticket "{ticket.title}" added successfully')
        return redirect(f'add_ticket')
    else:
        form = TicketForm()

    context = {
        'form': form,
        'title': 'Add ticket',
    }
    return render(request, 'accounting/add_ticket.html', context)


@login_required
def update_ticket(request, pk=None):
    """
    Function that allow user to update and complete specific ticket.

    Shows 'update_ticket' template with 'TicketForm' form.
    """
    ticket = get_object_or_404(Ticket, pk=pk, user=request.user, deleted=False)
    user_settings = UserSettings.objects.filter(user=request.user).get()

    form = TicketForm(instance=ticket)
    if request.method == 'POST':
        form = TicketForm(request.POST or None, instance=ticket)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.bought = round(ticket.bought, 2)
            if ticket.sold:
                ticket.sold = round(ticket.sold, 2)
                ticket.profit = round(ticket.sold - ticket.bought, 2)
                ticket.closed = 'True'
        ticket.save()
        messages.success(request, f'Ticket "{ticket.title}" successfully changed.')
        return redirect('home')

    context = {
        'form': form,
        'title': 'Update ticket',
        'ticket': ticket,
        'user_settings': user_settings,
    }
    return render(request, 'accounting/update_ticket.html', context)


@login_required
def delete_ticket(request, pk=None):
    """
    Function that allow user to delete specific ticket.
    """
    try:
        ticket = get_object_or_404(Ticket, pk=pk, user=request.user, deleted=False)
        if ticket:
            ticket.deleted = True
            ticket.save()
            messages.warning(request, f'Ticket "{ticket.title}" successfully deleted.')
    except Exception:
        messages.error(request, f'Ticket with ID: "{pk}" not found.')
    return redirect('home')
