import pytest

from django.urls import reverse

from accounting.management.commands.command_filter_query import FILTER_TICKETS
from accounting.models import Ticket
from tests.accounting.get_max_page import get_max_page
from tests.conftest import created_user, client


@pytest.mark.django_db
def test_view_tickets_check_tickets(
        created_user,
        login_user,
        client,
        add_ticket_filter,
        ticket,
        ticket_success,
        ticket_failure,
        ticket_without_profit,
):
    view_ticket_endpoint = reverse('home')
    response = client.get(view_ticket_endpoint)
    tickets = response.context.get('tickets')

    assert response.status_code == 200
    assert ticket in tickets
    assert ticket_success in tickets
    assert ticket_failure in tickets
    assert ticket_without_profit in tickets


@pytest.mark.django_db
def test_view_tickets_check_quantity(
        created_user,
        login_user,
        client,
        add_ticket_filter,
        ticket,
):
    view_ticket_endpoint = reverse('home')
    response = client.get(view_ticket_endpoint)
    tickets_quantity = response.context.get('tickets_quantity')

    assert tickets_quantity == Ticket.objects.all().count()


@pytest.mark.django_db
def test_view_tickets_check_ticket_filters(
        created_user,
        login_user,
        client,
        add_ticket_filter,
):
    view_ticket_endpoint = reverse('home')
    response = client.get(view_ticket_endpoint)
    ticket_filters = response.context.get('ticket_filter_query')

    for ticket_filter in FILTER_TICKETS:
        assert ticket_filters.filter(
            pk=ticket_filter.get('pk'),
            title=ticket_filter.get('title'),
            query_value=ticket_filter.get('query_value'),
            url_value=ticket_filter.get('url_value'),
            annotation=ticket_filter.get('annotation'),
            color=ticket_filter.get('color'),
        )


def test_view_tickets_not_auth_user_redirected(client):
    view_tickets_endpoint = reverse('home')
    response = client.get(view_tickets_endpoint)

    assert response.status_code == 302
    assert response.url == reverse('login')


@pytest.mark.django_db
def test_view_tickets_used_template(created_user, login_user, client, add_ticket_filter):
    view_tickets_endpoint = reverse('home')
    response = client.get(view_tickets_endpoint)

    assert 'accounting/index.html' in (template.name for template in response.templates)


@pytest.mark.django_db
def test_view_tickets_pagination_not_integer(
        created_user,
        login_user,
        client,
        add_ten_tickets,
        ticket,
        add_ticket_filter
):
    view_tickets_bad_endpoint = reverse('home') + '/?page=trigger_not_integer'
    view_tickets_good_endpoint_as = reverse('home') + '/?page=1'
    bad_response = client.get(view_tickets_bad_endpoint)
    good_response = client.get(view_tickets_good_endpoint_as)
    tickets_bad = bad_response.context.get('tickets')
    tickets_good = good_response.context.get('tickets')

    assert bad_response.status_code == 200
    assert good_response.status_code == 200
    assert tickets_bad.number == tickets_good.number


@pytest.mark.django_db
def test_view_tickets_pagination_empty_page(
        created_user,
        login_user,
        client,
        add_ten_tickets,
        ticket,
        add_ticket_filter,
):
    view_tickets_bad_endpoint = reverse('home') + '/?page=807583145'
    view_tickets_good_endpoint = reverse('home') + f'/?page={get_max_page(created_user)}'
    bad_response = client.get(view_tickets_bad_endpoint)
    good_response = client.get(view_tickets_good_endpoint)
    tickets_bad = bad_response.context.get('tickets')
    tickets_good = good_response.context.get('tickets')

    assert bad_response.status_code == 200
    assert good_response.status_code == 200
    assert tickets_bad.number == tickets_good.number

