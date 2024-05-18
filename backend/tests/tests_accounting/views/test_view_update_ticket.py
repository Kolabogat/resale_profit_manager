import pytest
from django.contrib.messages import get_messages
from django.urls import reverse

from accounting.models import Ticket


@pytest.mark.django_db
def test_update_ticket(
        logged_user,
        client,
        ticket,
):
    """
    HTTP METHOD: POST
    VIEW TESTED: update_ticket
    DESCRIPTION: status code is 302;
    ticket changed and exists; redirect to 'home';
    check alert message.
    """
    update_ticket_endpoint = reverse('update_ticket', args=[ticket.pk])
    ticket_title = 'Updated Ticket'
    response = client.post(
        update_ticket_endpoint,
        data={
            'title': ticket_title,
            'bought': ticket.bought,
            'sold': 6.36,
        })
    updated_ticket_exists = Ticket.objects.filter(
        title=ticket_title,
        bought=1.25,
        sold=6.36,
        profit=5.11,
    ).first()
    alert_message = f'Ticket "{ticket_title}" successfully changed.'
    response_message = str(list(get_messages(response.wsgi_request))[0])

    assert updated_ticket_exists
    assert response.status_code == 302
    assert response.url == reverse('home')
    assert alert_message in response_message


@pytest.mark.django_db
def test_update_ticket_used_template(
        logged_user,
        client,
        ticket,
):
    """
    HTTP METHOD: GET
    VIEW TESTED: update_ticket
    DESCRIPTION: template 'accounting/update_ticket.html' is used.
    """
    update_ticket_endpoint = reverse('update_ticket', args=[ticket.pk])
    response = client.get(update_ticket_endpoint)

    assert 'accounting/update_ticket.html' in (template.name for template in response.templates)


