from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import TicketForm
from .models import Ticket
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

FILTER_BY = {
    'waiting': 'profit_waiting',
    'failure': 'profit_failure',
    'nothing': 'profit_nothing',
    'success': 'profit_success',
    'bought_hl': 'bought_highest_to_lowest',
    'bought_lh': 'bought_lowest_to_highest',
    'sold_hl': 'sold_highest_to_lowest',
    'sold_lh': 'sold_lowest_to_highest',
    'profit_hl': 'profit_highest_to_lowest',
    'profit_lh': 'profit_lowest_to_highest',
    'date_oldest': 'date_oldest',
}


@login_required
def view_tickets(request, key=None):
    q = Q(user=request.user) & Q(deleted=False)
    get_query = request.GET.get('find')

    if get_query:
        q = q & Q(title__iregex=get_query)

    if key == 'profit_waiting':
        q = q & Q(profit=None)

    if key == 'profit_failure':
        q = q & Q(profit__lt=0)

    if key == 'profit_nothing':
        q = q & Q(profit=0)

    if key == 'profit_success':
        q = q & Q(profit__gt=0)

    tickets = Ticket.objects.filter(q)

    if key == 'bought_highest_to_lowest':
        tickets = tickets.order_by('-bought').values()

    if key == 'bought_lowest_to_highest':
        tickets = tickets.order_by('bought').values()

    if key == 'sold_highest_to_lowest':
        tickets = tickets.order_by('-sold').values()

    if key == 'sold_lowest_to_highest':
        tickets = tickets.order_by('sold').values()

    if key == 'profit_highest_to_lowest':
        tickets = tickets.order_by('-profit').values()

    if key == 'profit_lowest_to_highest':
        tickets = tickets.order_by('profit').values()

    if key == 'date_oldest':
        tickets = tickets.order_by('created_at').values()

    tickets_quantity = tickets.count()
    page = request.GET.get('page', 1)
    paginator = Paginator(tickets, 10)
    try:
        tickets = paginator.page(page)
    except PageNotAnInteger:
        tickets = paginator.page(1)
    except EmptyPage:
        tickets = paginator.page(paginator.num_pages)

    context = {
        'tickets': tickets,
        'tickets_quantity': tickets_quantity,
        'filter_by': FILTER_BY,
        'title': 'Tickets',
    }
    return render(request, 'accounting/index.html', context=context)


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
        messages.success(request, 'Ticket added successfully')
        return redirect(f'add_ticket')
    else:
        form = TicketForm()

    context = {
        'form': form,
    }
    return render(request, 'accounting/add_ticket.html', context)


@login_required
def update_ticket(request, id=None):
    obj = get_object_or_404(Ticket, id=id, user=request.user, deleted=False)
    form = TicketForm(instance=obj)
    if request.method == "POST":
        form = TicketForm(request.POST or None, instance=obj)
        if form.is_valid():
            ticket = form.save(commit=False)
            if ticket.sold:
                ticket.profit = round(ticket.sold - ticket.bought, 2)
                ticket.closed = 'True'
            ticket.save()
            messages.success(request, 'Ticket successfully changed.')
            return redirect('home')

    context = {
        "form": form,
    }
    return render(request, 'accounting/update_ticket.html', context)
