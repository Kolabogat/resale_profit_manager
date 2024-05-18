import pytest
from django.urls import reverse

from backend.settings import FILTER_TICKETS
from accounting.models import Ticket


@pytest.mark.django_db
def test_view_tickets_check_tickets(
        logged_user,
        client,
        add_all_tickets,
):
    """
    HTTP METHOD: GET
    VIEW TESTED: view_tickets
    DESCRIPTION: status code is 200; all tickets that
    should be displayed are on the main page.
    """
    view_ticket_endpoint = reverse('home')
    response = client.get(view_ticket_endpoint)
    tickets = response.context.get('tickets')

    assert response.status_code == 200
    assert add_all_tickets.get('ticket') in tickets
    assert add_all_tickets.get('ticket_success') in tickets
    assert add_all_tickets.get('ticket_failure') in tickets
    assert add_all_tickets.get('ticket_without_profit') in tickets


@pytest.mark.django_db
def test_view_tickets_check_quantity(
        logged_user,
        client,
        add_all_tickets,
):
    """
    HTTP METHOD: GET
    VIEW TESTED: view_tickets
    DESCRIPTION: quantity of tickets on the main page
    is equal to the quantity of tickets in database.
    """
    view_ticket_endpoint = reverse('home')
    response = client.get(view_ticket_endpoint)
    tickets_quantity = response.context.get('tickets_quantity')

    assert tickets_quantity == Ticket.objects.all().count()


@pytest.mark.django_db
def test_view_tickets_check_ticket_filters(
        logged_user,
        client,
):
    """
    HTTP METHOD: GET
    VIEW TESTED: view_tickets
    DESCRIPTION: checks that all filters are on the main page.
    """
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


def test_view_tickets_not_auth_user_redirected(
        client,
):
    """
    HTTP METHOD: GET
    VIEW TESTED: view_tickets
    DESCRIPTION: status code is 200; redirect
    unauthorized user to login page.
    """
    view_tickets_endpoint = reverse('home')
    response = client.get(view_tickets_endpoint)

    assert response.status_code == 302
    assert response.url == reverse('login')


@pytest.mark.django_db
def test_view_tickets_used_template(
        logged_user,
        client,
):
    """
    HTTP METHOD: GET
    VIEW TESTED: view_tickets
    DESCRIPTION: template 'accounting/index.html' is used.
    """
    view_tickets_endpoint = reverse('home')
    response = client.get(view_tickets_endpoint)

    assert 'accounting/index.html' in (template.name for template in response.templates)


@pytest.mark.django_db
def test_view_tickets_pagination_not_integer(
        logged_user,
        client,
        add_ten_tickets,
        ticket,
):
    """
    HTTP METHOD: GET
    VIEW TESTED: view_tickets
    DESCRIPTION: status code is 200;
    if value is not a number, first page is displayed.
    """
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
        logged_user,
        client,
        add_ten_tickets,
        ticket,
        get_max_page,
):
    """
    HTTP METHOD: GET
    VIEW TESTED: view_tickets
    DESCRIPTION: status code is 200;
    if value is a non-existent page, the first page is displayed.
    """
    view_tickets_bad_endpoint = reverse('home') + '/?page=807583145'
    view_tickets_good_endpoint = reverse('home') + f'/?page={get_max_page}'
    bad_response = client.get(view_tickets_bad_endpoint)
    good_response = client.get(view_tickets_good_endpoint)
    tickets_bad = bad_response.context.get('tickets')
    tickets_good = good_response.context.get('tickets')

    assert bad_response.status_code == 200
    assert good_response.status_code == 200
    assert tickets_bad.number == tickets_good.number

