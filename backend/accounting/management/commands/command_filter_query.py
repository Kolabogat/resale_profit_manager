from django.core.management.base import BaseCommand
from backend.settings import FILTER_TICKETS
from ...models import TicketFilter


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

