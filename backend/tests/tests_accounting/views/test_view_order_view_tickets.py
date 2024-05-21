import pytest
from django.db.models import Q
from django.urls import reverse

from accounting.models import Ticket


@pytest.mark.django_db
def test_view_tickets_filter_asc_bought(
        logged_user,
        client,
        add_all_tickets,
):
    view_tickets_filter_endpoint = reverse('home') + '/?order_by=bought_asc'
    response = client.get(view_tickets_filter_endpoint)
    tickets = response.context.get('tickets')

    tickets_query = Ticket.objects.filter(
        Q(user=logged_user) &
        Q(deleted=False)
    ).order_by('bought')
    tickets_quantity = tickets_query.count()

    assert response.status_code == 200
    for index in range(tickets_quantity):
        assert tickets_query[index].id == tickets[index].get('id')


@pytest.mark.django_db
def test_view_tickets_filter_desc_bought(
        logged_user,
        client,
        add_all_tickets,
):
    view_tickets_filter_endpoint = reverse('home') + '/?order_by=bought_desc'
    response = client.get(view_tickets_filter_endpoint)
    tickets = response.context.get('tickets')

    tickets_query = Ticket.objects.filter(
        Q(user=logged_user) &
        Q(deleted=False) &
        ~Q(profit=None)
    ).order_by('-bought')
    tickets_quantity = tickets_query.count()

    assert response.status_code == 200
    for index in range(tickets_quantity):
        assert tickets_query[index].id == tickets[index].get('id')


@pytest.mark.django_db
def test_view_tickets_filter_asc_sold(
        logged_user,
        client,
        add_all_tickets,
):
    view_tickets_filter_endpoint = reverse('home') + '/?order_by=sold_asc'
    response = client.get(view_tickets_filter_endpoint)
    tickets = response.context.get('tickets')

    tickets_query = Ticket.objects.filter(
        Q(user=logged_user) &
        Q(deleted=False) &
        ~Q(profit=None)
    ).order_by('sold')
    tickets_quantity = tickets_query.count()

    assert response.status_code == 200
    for index in range(tickets_quantity):
        assert tickets_query[index].id == tickets[index].get('id')


@pytest.mark.django_db
def test_view_tickets_filter_desc_sold(
        logged_user,
        client,
        add_all_tickets,
):
    view_tickets_filter_endpoint = reverse('home') + '/?order_by=sold_desc'
    response = client.get(view_tickets_filter_endpoint)
    tickets = response.context.get('tickets')

    tickets_query = Ticket.objects.filter(
        Q(user=logged_user) &
        Q(deleted=False) &
        ~Q(profit=None)
    ).order_by('-sold')
    tickets_quantity = tickets_query.count()

    assert response.status_code == 200
    for index in range(tickets_quantity):
        assert tickets_query[index].id == tickets[index].get('id')


@pytest.mark.django_db
def test_view_tickets_filter_asc_profit(
        logged_user,
        client,
        add_all_tickets,
):
    view_tickets_filter_endpoint = reverse('home') + '/?order_by=profit_asc'
    response = client.get(view_tickets_filter_endpoint)
    tickets = response.context.get('tickets')

    tickets_query = Ticket.objects.filter(
        Q(user=logged_user) &
        Q(deleted=False) &
        ~Q(profit=None)
    ).order_by('profit')
    tickets_quantity = tickets_query.count()

    assert response.status_code == 200
    for index in range(tickets_quantity):
        assert tickets_query[index].id == tickets[index].get('id')


@pytest.mark.django_db
def test_view_tickets_filter_desc_profit(
        logged_user,
        client,
        add_all_tickets,
):
    view_tickets_filter_endpoint = reverse('home') + '/?order_by=profit_desc'
    response = client.get(view_tickets_filter_endpoint)
    tickets = response.context.get('tickets')

    tickets_query = Ticket.objects.filter(
        Q(user=logged_user) &
        Q(deleted=False) &
        ~Q(profit=None)
    ).order_by('-profit')
    tickets_quantity = tickets_query.count()

    assert response.status_code == 200
    for index in range(tickets_quantity):
        assert tickets_query[index].id == tickets[index].get('id')


@pytest.mark.django_db
def test_view_tickets_filter_date(
        logged_user,
        client,
        add_all_tickets,
):
    view_tickets_filter_endpoint = reverse('home') + '/?order_by=date_asc'
    response = client.get(view_tickets_filter_endpoint)
    tickets = response.context.get('tickets')

    tickets_query = Ticket.objects.filter(
        Q(user=logged_user) &
        Q(deleted=False)
    ).order_by('created_at')
    tickets_quantity = tickets_query.count()

    assert response.status_code == 200
    for index in range(tickets_quantity):
        assert tickets_query[index].id == tickets[index].get('id')
