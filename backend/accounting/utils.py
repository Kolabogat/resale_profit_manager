from django.db.models import Q

from accounting.models import Ticket
from backend.const import TICKETS_FILTER_STATE, TICKET_FILTERS_ORDER_BY


def tickets_filter(request, search_filter, filter_by):
    """
    Accepts values: request, search_filter, filter_by.
    Where  search_filter - search word,
    filter_by - specific filter word.

    Function at first checks if 'search_filter' exists
    and then checks if there is a 'filter_by' filter exist in constant.
    """
    q = Q(user=request.user) & Q(deleted=False)

    if search_filter:
        q = q & Q(title__iregex=search_filter)

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

    tickets = Ticket.objects.filter(q)

    for ticket_filter in TICKET_FILTERS_ORDER_BY:
        if filter_by == ticket_filter.get('url_value'):
            if 'sold' in filter_by or 'profit' in filter_by:
                tickets = tickets.filter(~Q(profit=None))
            tickets = tickets.order_by(ticket_filter.get('query_value')).values()

    return tickets
