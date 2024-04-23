from django.contrib.auth.models import User
import pytest

from accounting.management.commands.command_filter_query import FILTER_TICKETS
from accounting.models import Ticket, TicketFilter
from user.models import UserSettings, UserProfile
from datetime import datetime
from selenium import webdriver


@pytest.fixture
def user():
    user = User.objects.create_user(
        username='user',
        email='user@user.com',
        password='a9Jd2o9gLe2axs',
    )
    UserSettings.objects.create(user=user)
    UserProfile.objects.create(user=user)
    return user


@pytest.fixture
def ticket(user):
    ticket = Ticket.objects.create(
        user=user,
        title='Name of ticket',
        closed=False,
        bought=5.12,
        sold=6.31,
        profit=None,
        created_at=datetime.now(),
        closed_at=datetime.now(),
        deleted=False,
    )
    return ticket


@pytest.fixture
def add_ticket_filter():
    for filter_dict in FILTER_TICKETS:
        if not TicketFilter.objects.filter(pk=filter_dict.get('pk')):
            filter_model = TicketFilter(**filter_dict)
            filter_model.save()


@pytest.fixture(scope='class')
def driver_init(request):
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    web_driver = webdriver.Chrome(options=options)
    request.cls.driver = web_driver
    yield
    web_driver.close()
