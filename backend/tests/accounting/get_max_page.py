from accounting.models import Ticket
from user.models import UserSettings


def get_max_page(created_user):
    user_settings = UserSettings.objects.filter(user=created_user).first()
    paginate_by = user_settings.paginate_by.paginate_by
    all_tickets = Ticket.objects.all().count()
    remainder = all_tickets % paginate_by
    result = all_tickets // paginate_by
    if remainder > 0:
        result += 1
    return result
