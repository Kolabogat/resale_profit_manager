from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import TicketForm
from .models import Ticket, TicketFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from user.models import UserSettings


def tickets_filter(request, ticket_filter_query, search_filter, filter_by):
    """
    Accepts values: request, ticket_query, search_filter, filter_by.
    Where ticket_filter_query - all filters from DB,
    search_filter - search word, filter_by - specific filter world.

    Function at first checks if 'search_filter' exists
    and then checks if there is a 'filter_by' filter exist in database.
    """
    q = Q(user=request.user) & Q(deleted=False)

    if search_filter:
        q = q & Q(title__iregex=search_filter)

    if filter_by == ticket_filter_query.get(pk=1).url_value:
        q = q & Q(profit=None)

    if filter_by == ticket_filter_query.get(pk=2).url_value:
        q = q & Q(profit__lt=0)

    if filter_by == ticket_filter_query.get(pk=3).url_value:
        q = q & Q(profit=0)

    if filter_by == ticket_filter_query.get(pk=4).url_value:
        q = q & Q(profit__gt=0)

    tickets = Ticket.objects.filter(q)

    for id_number in range(5, 12):
        filter_value = ticket_filter_query.get(pk=id_number)
        if filter_by == filter_value.url_value:
            if filter_value.title != 'Date':
                tickets = tickets.filter(~Q(profit=None))
            tickets = tickets.order_by(filter_value.query_value).values()

    return tickets


def view_tickets(request):
    """
    Function that allow user to add waiting or completed ticket.

    Pagination value is taken from individual 'UserSettings' settings.

    Show tickets without any filters. If 'filter_by' filters or
    'search_filter' searches are received then check
    the filters in the 'tickets_filter' function.

    Show 'login' template if user not authenticated.
    """
    if request.user.is_authenticated:
        search_filter = request.GET.get('search')
        filter_by = request.GET.get('filter_by')
        ticket_filter_query = TicketFilter.objects.all()
        user_additional = UserSettings.objects.filter(user=request.user).get()
        paginate_by = str(user_additional.paginate_by)

        tickets = tickets_filter(request, ticket_filter_query, search_filter, filter_by)

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
            'ticket_filter_query': ticket_filter_query,
            'user_additional': user_additional,
            'title': 'Tickets',
        }
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
        messages.success(request, f'Ticket "{ticket.title}"  added successfully')
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
