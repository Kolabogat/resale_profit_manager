from django.core.management.base import BaseCommand

from ...models import TicketFilter
from time import sleep

FILTER_TICKETS = (
    {
        'pk': 1,
        'title': 'Profit Waiting',
        'query_value': '',
        'url_value': 'profit_waiting',
        'annotation': 'Filter tickets by profit none',
        'color': '#f6d6ad'
    },
    {
        'pk': 2,
        'title': 'Profit Failure',
        'query_value': '',
        'url_value': 'profit_failure',
        'annotation': 'Filter tickets by profit failure',
        'color': '#f9c0c0'
    },
    {
        'pk': 3,
        'title': 'Profit Nothing',
        'query_value': '',
        'url_value': 'profit_nothing',
        'annotation': 'Filter tickets without profit',
        'color': '#fafcc2'
    },
    {
        'pk': 4,
        'title': 'Profit Success',
        'query_value': '',
        'url_value': 'profit_success',
        'annotation': 'Filter tickets by profit success',
        'color': '#ccf6c8'
    },
    {
        'pk': 5,
        'title': 'Ascending Bought',
        'query_value': 'bought',
        'url_value': 'bought_asc',
        'annotation': 'Filter tickets by bought from lowest to highest',
        'color': '#ffd571'
    },
    {
        'pk': 6,
        'title': 'Descending Bought',
        'query_value': '-bought',
        'url_value': 'bought_desc',
        'annotation': 'Filter tickets by bought from highest to lowest',
        'color': '#f4ebc1'
    },
    {
        'pk': 7,
        'title': 'Ascending Sold',
        'query_value': 'sold',
        'url_value': 'sold_asc',
        'annotation': 'Filter tickets by sold from lowest to highest',
        'color': '#ffd571'
    },
    {
        'pk': 8,
        'title': 'Descending Sold',
        'query_value': '-sold',
        'url_value': 'sold_desc',
        'annotation': 'Filter tickets by sold from highest to lowest',
        'color': '#f4ebc1'
    },

    {
        'pk': 9,
        'title': 'Ascending Profit',
        'query_value': 'profit',
        'url_value': 'profit_asc',
        'annotation': 'Filter tickets by profit from lowest to highest',
        'color': '#ffd571'
    },
    {
        'pk': 10,
        'title': 'Descending Profit',
        'query_value': '-profit',
        'url_value': 'profit_desc',
        'annotation': 'Filter tickets by profit from highest to lowest',
        'color': '#f4ebc1'
    },
    {
        'pk': 11,
        'title': 'Date',
        'query_value': 'created_at',
        'url_value': 'date',
        'annotation': 'Filter tickets by earliest date',
        'color': '#ff9a76'
    },
)


class Command(BaseCommand):
    help = """
    Command that uploads constants that are needed for links, 
    filter values, styles, descriptions, filter names.
    """

    def handle(self, *args, **options):
        for filter_dict in FILTER_TICKETS:
            title = filter_dict.get('title')
            if not TicketFilter.objects.filter(pk=filter_dict.get('pk')):
                filter_model = TicketFilter(**filter_dict)
                filter_model.save()
                self.stdout.write(f'Filter "{title}" added.')
            else:
                self.stdout.write(f'Filter "{title}" already exist.')
        return self.stdout.write(f'Command completed!')

