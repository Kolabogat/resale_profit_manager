import pytest
from django.db.models import Q
from accounting.models import Ticket
from django.db.models import Sum, Max, Min


@pytest.fixture
def get_updated_user_profile(
        created_user
):
    q = Q(user=created_user) & Q(deleted=False)
    tickets = Ticket.objects.filter(q)

    all_time_profit = round(tickets.aggregate(Sum('profit')).get('profit__sum'), 2)
    tickets_quantity = tickets.count()
    highest_profit = round(tickets.aggregate(Max('profit')).get('profit__max'), 2)
    highest_loss = round(tickets.aggregate(Min('profit')).get('profit__min'), 2)

    highest_profit = (highest_profit if highest_profit >= 0 else 0)
    highest_loss = highest_loss if highest_loss <= 0 else 0

    return {
        'all_time_profit': all_time_profit,
        'tickets_quantity': tickets_quantity,
        'highest_profit': highest_profit,
        'highest_loss': highest_loss,
    }
