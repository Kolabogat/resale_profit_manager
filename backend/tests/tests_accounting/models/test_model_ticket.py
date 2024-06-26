import pytest

from accounting.models import Ticket


@pytest.mark.django_db
def test_ticket_created(
        created_user,
        ticket,
):
    ticket_object = Ticket.objects.filter(
        user=ticket.user,
        title=ticket.title,
        closed=False,
        bought=ticket.bought,
        sold=ticket.sold,
        profit=ticket.profit,
        deleted=False,
    ).first()
    ticket_objects = Ticket.objects.all()
    assert ticket_object in ticket_objects


@pytest.mark.django_db
def test_ticket_update(
        created_user,
        ticket,
):
    ticket.title = 'New Title'
    ticket.bought = 4
    ticket.sold = 5
    ticket.profit = 1
    ticket.save()
    ticket_objects = Ticket.objects.all()

    assert ticket in ticket_objects


@pytest.mark.django_db
def test_ticket_model_update_url(
        created_user,
        ticket,
):
    update_url = Ticket.get_update_url(ticket)

    assert update_url == f'/update/{ticket.pk}'


@pytest.mark.django_db
def test_ticket_model_delete_url(
        created_user,
        ticket,
):
    delete_url = Ticket.get_delete_url(ticket)

    assert delete_url == f'/delete/{ticket.pk}'


@pytest.mark.django_db
def test_ticket_model_str_method(
        created_user,
        ticket,
):
    str_method = Ticket.__str__(ticket)

    assert str_method == f'{ticket.title}'
