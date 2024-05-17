from django.db.models import Q

from accounting.models import Ticket


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
