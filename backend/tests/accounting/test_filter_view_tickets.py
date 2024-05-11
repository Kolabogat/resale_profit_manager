import pytest
from django.db.models import Q

from django.urls import reverse

from accounting.models import Ticket
from tests.conftest import created_user, client


@pytest.mark.django_db
def test_view_tickets_filter_profit_waiting(
        created_user,
        login_user,
        client,
        add_ticket_filter,
        add_ten_tickets,
        ticket,
        ticket_success,
        ticket_failure,
        ticket_without_profit,
):
    view_tickets_filter_endpoint = reverse('home') + '/?filter_by=profit_waiting'
    response = client.get(view_tickets_filter_endpoint)
    tickets = response.context.get('tickets')

    tickets_query = Ticket.objects.filter(
        Q(user=created_user) &
        Q(deleted=False) &
        Q(profit=None)
    )
    assert response.status_code == 200
    for ticket_object in tickets:
        assert ticket_object in tickets_query


@pytest.mark.django_db
def test_view_tickets_filter_profit_failure(
        created_user,
        login_user,
        client,
        add_ticket_filter,
        add_ten_tickets,
        ticket,
        ticket_success,
        ticket_failure,
        ticket_without_profit,
):
    view_tickets_filter_endpoint = reverse('home') + '/?filter_by=profit_failure'
    response = client.get(view_tickets_filter_endpoint)
    tickets = response.context.get('tickets')

    tickets_query = Ticket.objects.filter(
        Q(user=created_user) &
        Q(deleted=False) &
        Q(profit__lt=0)
    )
    assert response.status_code == 200
    for ticket_object in tickets:
        assert ticket_object in tickets_query


@pytest.mark.django_db
def test_view_tickets_filter_profit_nothing(
        created_user,
        login_user,
        client,
        add_ticket_filter,
        add_ten_tickets,
        ticket,
        ticket_success,
        ticket_failure,
        ticket_without_profit,
):
    view_tickets_filter_endpoint = reverse('home') + '/?filter_by=profit_nothing'
    response = client.get(view_tickets_filter_endpoint)
    tickets = response.context.get('tickets')

    tickets_query = Ticket.objects.filter(
        Q(user=created_user) &
        Q(deleted=False) &
        Q(profit=0)
    )
    assert response.status_code == 200
    for ticket_object in tickets:
        assert ticket_object in tickets_query


@pytest.mark.django_db
def test_view_tickets_filter_profit_success(
        created_user,
        login_user,
        client,
        add_ticket_filter,
        add_ten_tickets,
        ticket,
        ticket_success,
        ticket_failure,
        ticket_without_profit,
):
    view_tickets_filter_endpoint = reverse('home') + '/?filter_by=profit_success'
    response = client.get(view_tickets_filter_endpoint)
    tickets = response.context.get('tickets')

    tickets_query = Ticket.objects.filter(
        Q(user=created_user) &
        Q(deleted=False) &
        Q(profit__gt=0)
    )
    assert response.status_code == 200
    for ticket_object in tickets:
        assert ticket_object in tickets_query



