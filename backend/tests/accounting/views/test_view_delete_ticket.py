import pytest

from django.contrib.messages import get_messages
from django.urls import reverse

from accounting.models import Ticket
from tests.conftest import created_user, client


@pytest.mark.django_db
def test_delete_ticket(created_user, login_user, client, ticket):
    delete_ticket_endpoint = reverse('delete_ticket', args=[ticket.pk])
    response = client.get(delete_ticket_endpoint)
    deleted_ticket_exists = Ticket.objects.filter(
        title=ticket.title,
        bought=ticket.bought,
        deleted=True,
    ).exists()
    alert_message = f'Ticket "{ticket.title}" successfully deleted.'
    response_message = str(list(get_messages(response.wsgi_request))[0])

    assert response.status_code == 302
    assert deleted_ticket_exists
    assert response.url == reverse('home')
    assert alert_message in response_message


@pytest.mark.django_db
def test_delete_ticket_not(created_user, login_user, client):
    ticket_pk = 2345756
    delete_ticket_endpoint = reverse('delete_ticket', args=[ticket_pk])
    response = client.get(delete_ticket_endpoint)
    alert_message = f'Ticket with ID: "{ticket_pk}" not found.'
    response_message = str(list(get_messages(response.wsgi_request))[0])

    assert response.status_code == 302
    assert response.url == reverse('home')
    assert alert_message in response_message
