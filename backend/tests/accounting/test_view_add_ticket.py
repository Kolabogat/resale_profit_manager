import pytest

from django.contrib.messages import get_messages
from django.urls import reverse

from accounting.models import Ticket
from tests.conftest import created_user, client


@pytest.mark.django_db
def test_add_ticket_of_waiting(created_user, register_user, client):
    add_ticket_endpoint = reverse('add_ticket')
    ticket_title = 'Test Ticket of Waiting'
    response = client.post(
        add_ticket_endpoint,
        data={
            'title': ticket_title,
            'bought': 5.67,
        })
    new_ticket_exists = Ticket.objects.filter(
        title=ticket_title,
        bought=5.67,
        sold=None,
        profit=None,
    ).exists()
    alert_message = f'Ticket "{ticket_title}" added successfully'
    response_message = str(list(get_messages(response.wsgi_request))[0])

    assert new_ticket_exists
    assert response.status_code == 302
    assert response.url == reverse('add_ticket')
    assert alert_message in response_message


@pytest.mark.django_db
def test_add_ticket_of_success(created_user, register_user, client):
    add_ticket_endpoint = reverse('add_ticket')
    ticket_title = 'Test Ticket of Success'
    response = client.post(
        add_ticket_endpoint,
        data={
            'title': ticket_title,
            'bought': 5.67,
            'sold': 6.00,
        })
    new_ticket_exists = Ticket.objects.filter(
        title=ticket_title,
        bought=5.67,
        sold=6.00,
        profit=0.33,
    ).exists()
    alert_message = f'Ticket "{ticket_title}" added successfully'
    response_message = str(list(get_messages(response.wsgi_request))[0])

    assert new_ticket_exists
    assert response.status_code == 302
    assert response.url == reverse('add_ticket')
    assert alert_message in response_message


@pytest.mark.django_db
def test_add_ticket_of_failure(created_user, register_user, client):
    add_ticket_endpoint = reverse('add_ticket')
    ticket_title = 'Test Ticket of Failure'
    response = client.post(
        add_ticket_endpoint,
        data={
            'title': ticket_title,
            'bought': 5.67,
            'sold': 5.21,
        })
    new_ticket_exists = Ticket.objects.filter(
        title=ticket_title,
        bought=5.67,
        sold=5.21,
        profit=-0.46,
    ).exists()
    alert_message = f'Ticket "{ticket_title}" added successfully'
    response_message = str(list(get_messages(response.wsgi_request))[0])

    assert new_ticket_exists
    assert response.status_code == 302
    assert response.url == reverse('add_ticket')
    assert alert_message in response_message


@pytest.mark.django_db
def test_add_ticket_of_nothing(created_user, register_user, client):
    add_ticket_endpoint = reverse('add_ticket')
    ticket_title = 'Test Ticket of Nothing'
    response = client.post(
        add_ticket_endpoint,
        data={
            'title': ticket_title,
            'bought': 5.67,
            'sold': 5.67,
        })
    new_ticket_exists = Ticket.objects.filter(
        title=ticket_title,
        bought=5.67,
        sold=5.67,
        profit=0,
    ).exists()
    alert_message = f'Ticket "{ticket_title}" added successfully'
    response_message = str(list(get_messages(response.wsgi_request))[0])

    assert new_ticket_exists
    assert response.status_code == 302
    assert response.url == reverse('add_ticket')
    assert alert_message in response_message


@pytest.mark.django_db
def test_add_ticket_used_template(created_user, register_user, client):
    add_ticket_endpoint = reverse('add_ticket')
    response = client.get(add_ticket_endpoint)

    assert 'accounting/add_ticket.html' in (template.name for template in response.templates)