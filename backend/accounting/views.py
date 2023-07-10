from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import TicketForm
from .models import Ticket, TicketFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from user.models import UserAdditional

def tickets_filter(request, ticket_filter_query, search_filter, filter_by):
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
            tickets = tickets.order_by(filter_value.query_value).values()

    return tickets


def view_tickets(request):
    if request.user.is_authenticated:
        search_filter = request.GET.get('search')
        filter_by = request.GET.get('filter_by')
        ticket_filter_query = TicketFilter.objects.all()
        paginate_by = UserAdditional.objects.filter(user=request.user).get().paginate_by

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
            'title': 'Tickets',
        }
        return render(request, 'accounting/index.html', context=context)
    else:
        return redirect('login')


@login_required
def add_ticket(request):
    form = TicketForm(request.POST or None)

    if form.is_valid():
        ticket = form.save(commit=False)
        ticket.user = request.user
        if ticket.sold:
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
    ticket = get_object_or_404(Ticket, pk=pk, user=request.user, deleted=False)
    form = TicketForm(instance=ticket)
    if request.method == 'POST':
        form = TicketForm(request.POST or None, instance=ticket)
        if form.is_valid():
            ticket = form.save(commit=False)
            if ticket.sold:
                ticket.profit = round(ticket.sold - ticket.bought, 2)
                ticket.closed = 'True'
            ticket.save()
            messages.success(request, f'Ticket "{ticket.title}" successfully changed.')
            return redirect('home')

    context = {
        'form': form,
        'title': 'Update ticket',
        'ticket': ticket
    }
    return render(request, 'accounting/update_ticket.html', context)


@login_required
def delete_ticket(request, pk=None):
    try:
        ticket = get_object_or_404(Ticket, pk=pk, user=request.user, deleted=False)
        if ticket:
            ticket.deleted = True
            ticket.save()
            messages.warning(request, f'Ticket "{ticket.title}" successfully deleted.')
    except Exception:
        messages.error(request, f'Ticket with ID: "{pk}" not found.')
    return redirect('home')
