from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import TicketForm
from .models import Ticket
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def view_tickets(request):
    ticket_item = Ticket.objects.filter(user=request.user)
    page = request.GET.get('page', 1)
    paginator = Paginator(ticket_item, 5)

    try:
        tickets = paginator.page(page)
    except PageNotAnInteger:
        tickets = paginator.page(1)
    except EmptyPage:
        tickets = paginator.page(paginator.num_pages)

    context = {
        'tickets': tickets,
        'title': 'Tickets',
    }
    return render(request, 'accounting/index.html', context=context)


def view_about(request):
    return render(request, 'accounting/about.html')


@login_required
def add_ticket(request):
    form = TicketForm(request.POST or None)

    if form.is_valid():
        ticket = form.save(commit=False)
        ticket.user = request.user
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
    obj = get_object_or_404(Ticket, id=id, user=request.user)
    form = TicketForm(instance=obj)
    if request.method == "POST":
        form = TicketForm(request.POST or None, instance=obj)
        if form.is_valid():
            form = form.save(commit=False)
            if form.sold:
                form.profit = round(form.sold - form.bought, 2)
                form.closed = 'True'
            form.save()
            messages.success(request, 'Ticket successfully changed.')
            return redirect('home')

    context = {
        "form": form,
    }
    return render(request, 'accounting/update_ticket.html', context)
