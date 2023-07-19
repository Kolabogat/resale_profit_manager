from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import random
from accounting.models import Ticket


class Command(BaseCommand):
    help = """
    Command that creates tickets for superuser.
    """

    def handle(self, *args, **options):
        user = User.objects.filter(username='admin').get()
        for number in range(200):
            title = f'Ticket {number}'
            bought = random.randrange(1, 50)
            sold = random.choice([False, random.randrange(1, 70)])

            ticket = Ticket(
                user=user,
                title=title,
                bought=bought,
                sold=sold,
                profit=(round(sold - bought, 2) if sold else None),
            )
            ticket.save()
        return self.stdout.write(f'Tickets created.')
