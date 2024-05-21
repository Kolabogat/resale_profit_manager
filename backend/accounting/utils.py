from django.db.models import Q

from accounting.models import Ticket
from backend.const import TICKETS_FILTER_STATE, TICKET_FILTERS_ORDER_BY


def get_filtered_tickets(request, search, filter_by, order_by):
    """
    Accepts values: request, search, filter_by, order_by.
    Where  search_filter - search word,
    filter_by - specific filter word,
    order_by - specific order word.

    Function at first checks if 'search' exists
    and then checks if there is a 'filter_by' or
    'order_by' filter exist in constants.
    """
    q = Q(user=request.user) & Q(deleted=False)
    if search:
        q = q & tickets_search(search, q)
    if filter_by:
        q = q & tickets_filter(filter_by, q)
    if order_by:
        tickets = tickets_order(order_by, q)
    else:
        tickets = Ticket.objects.filter(q)
    return tickets


def tickets_search(search, q):
    q = q & Q(title__iregex=search)
    return q


def tickets_filter(filter_by, q):
    for ticket_filter in TICKETS_FILTER_STATE:
        filter_url = ticket_filter.get('url_value')
        if filter_by == filter_url:
            if filter_url == 'profit_waiting':
                q = q & Q(profit=None)
            if filter_url == 'profit_failure':
                q = q & Q(profit__lt=0)
            if filter_url == 'profit_nothing':
                q = q & Q(profit=0)
            if filter_url == 'profit_success':
                q = q & Q(profit__gt=0)
    return q


def tickets_order(order_by, q):
    tickets = Ticket.objects.filter(q)
    for ticket_filter in TICKET_FILTERS_ORDER_BY:
        if order_by == ticket_filter.get('url_value'):
            if 'sold' in order_by or 'profit' in order_by:
                tickets = tickets.filter(~Q(profit=None))
            tickets = tickets.order_by(ticket_filter.get('query_value')).values()
    return tickets
