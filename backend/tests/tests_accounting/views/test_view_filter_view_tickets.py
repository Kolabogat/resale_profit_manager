import pytest
from django.db.models import Q

from django.urls import reverse

from accounting.models import Ticket
from tests.conftest import logged_user, client, add_all_tickets, add_ten_tickets


@pytest.mark.django_db
def test_view_tickets_filter_profit_waiting(
        client,
        logged_user,
        add_all_tickets,
        add_ten_tickets,
):
    view_tickets_filter_endpoint = reverse('home') + '/?filter_by=profit_waiting'
    response = client.get(view_tickets_filter_endpoint)
    tickets = response.context.get('tickets')

    tickets_query = Ticket.objects.filter(
        Q(user=logged_user) &
        Q(deleted=False) &
        Q(profit=None)
    )
    assert response.status_code == 200
    for ticket_object in tickets:
        assert ticket_object in tickets_query


@pytest.mark.django_db
def test_view_tickets_filter_profit_failure(
        client,
        logged_user,
        add_all_tickets,
        add_ten_tickets,
):
    view_tickets_filter_endpoint = reverse('home') + '/?filter_by=profit_failure'
    response = client.get(view_tickets_filter_endpoint)
    tickets = response.context.get('tickets')

    tickets_query = Ticket.objects.filter(
        Q(user=logged_user) &
        Q(deleted=False) &
        Q(profit__lt=0)
    )
    assert response.status_code == 200
    for ticket_object in tickets:
        assert ticket_object in tickets_query


@pytest.mark.django_db
def test_view_tickets_filter_profit_nothing(
        client,
        logged_user,
        add_all_tickets,
        add_ten_tickets,
):
    view_tickets_filter_endpoint = reverse('home') + '/?filter_by=profit_nothing'
    response = client.get(view_tickets_filter_endpoint)
    tickets = response.context.get('tickets')

    tickets_query = Ticket.objects.filter(
        Q(user=logged_user) &
        Q(deleted=False) &
        Q(profit=0)
    )
    assert response.status_code == 200
    for ticket_object in tickets:
        assert ticket_object in tickets_query


@pytest.mark.django_db
def test_view_tickets_filter_profit_success(
        client,
        logged_user,
        add_all_tickets,
        add_ten_tickets,
):
    view_tickets_filter_endpoint = reverse('home') + '/?filter_by=profit_success'
    response = client.get(view_tickets_filter_endpoint)
    tickets = response.context.get('tickets')

    tickets_query = Ticket.objects.filter(
        Q(user=logged_user) &
        Q(deleted=False) &
        Q(profit__gt=0)
    )
    assert response.status_code == 200
    for ticket_object in tickets:
        assert ticket_object in tickets_query



