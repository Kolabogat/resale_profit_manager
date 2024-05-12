import pytest
from django.db.models import Q

from django.urls import reverse


from accounting.models import Ticket
from tests.conftest import created_user, client


@pytest.mark.django_db
def test_view_tickets_search_one_word(
        created_user,
        login_user,
        client,
        add_ticket_filter,
        ticket,
        ticket_success,
        ticket_failure,
        ticket_without_profit,
        add_ten_tickets,
):
    search_filter = 'wait'
    view_tickets_filter_endpoint = reverse('home') + f'/?search={search_filter}'
    response = client.get(view_tickets_filter_endpoint)
    tickets = response.context.get('tickets')

    tickets_query = Ticket.objects.filter(
        Q(user=created_user) &
        Q(deleted=False) &
        Q(title__iregex=search_filter)
    )

    assert response.status_code == 200
    for ticket_object in tickets:
        assert ticket_object in tickets_query


@pytest.mark.django_db
def test_view_tickets_search_two_words(
        created_user,
        login_user,
        client,
        add_ticket_filter,
        ticket,
        ticket_success,
        ticket_failure,
        ticket_without_profit,
        add_ten_tickets,
):
    search_filter = 'Ticket of'
    view_tickets_filter_endpoint = reverse('home') + f'/?search={search_filter}'
    response = client.get(view_tickets_filter_endpoint)
    tickets = response.context.get('tickets')

    tickets_query = Ticket.objects.filter(
        Q(user=created_user) &
        Q(deleted=False) &
        Q(title__iregex=search_filter)
    )

    assert response.status_code == 200
    for ticket_object in tickets:
        assert ticket_object in tickets_query


@pytest.mark.django_db
def test_view_tickets_search_number(
        created_user,
        login_user,
        client,
        add_ticket_filter,
        ticket,
        ticket_success,
        ticket_failure,
        ticket_without_profit,
        add_ten_tickets,
):
    search_filter = '5'
    view_tickets_filter_endpoint = reverse('home') + f'/?search={search_filter}'
    response = client.get(view_tickets_filter_endpoint)
    tickets = response.context.get('tickets')

    tickets_query = Ticket.objects.filter(
        Q(user=created_user) &
        Q(deleted=False) &
        Q(title__iregex=search_filter)
    )

    assert response.status_code == 200
    for ticket_object in tickets:
        assert ticket_object in tickets_query


@pytest.mark.django_db
def test_view_tickets_search_not_existing(
        created_user,
        login_user,
        client,
        add_ticket_filter,
):
    search_filter = 'not_existing_ticket_01'
    view_tickets_filter_endpoint = reverse('home') + f'/?search={search_filter}'
    response = client.get(view_tickets_filter_endpoint)
    tickets = response.context.get('tickets')

    tickets_query = Ticket.objects.filter(
        Q(user=created_user) &
        Q(deleted=False) &
        Q(title__iregex=search_filter)
    )
    assert response.status_code == 200
    assert not tickets_query.exists()
    assert not tickets.object_list.exists()

