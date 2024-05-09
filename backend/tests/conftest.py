import pytest

from django.contrib.auth.models import User
from user.models import UserSettings, UserProfile
from accounting.models import Ticket, TicketFilter
from accounting.management.commands.command_filter_query import FILTER_TICKETS


TEST_USERNAME = 'user'
TEST_PASSWORD = 'a9Jd2o9gLe2axs'
TEST_EMAIL = 'user@user.com'


@pytest.fixture
def user():
    user = User.objects.create_user(
        username=TEST_USERNAME,
        email=TEST_EMAIL,
        password=TEST_PASSWORD,
    )
    UserSettings.objects.create(user=user)
    UserProfile.objects.create(user=user)
    return user


@pytest.fixture
def ticket(user):
    ticket = Ticket.objects.create(
        user=user,
        title='Name of ticket',
        bought=5.12,
        sold=None,
        profit=None,
    )
    return ticket


@pytest.fixture
def add_ticket_filter():
    for filter_dict in FILTER_TICKETS:
        if not TicketFilter.objects.filter(pk=filter_dict.get('pk')):
            filter_model = TicketFilter(**filter_dict)
            filter_model.save()

