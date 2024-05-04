from django.test import TestCase
from django.contrib.auth.models import User

from accounting.management.commands.command_filter_query import FILTER_TICKETS
from accounting.models import Ticket, TicketFilter
from datetime import datetime


class TestTicketModels(TestCase):
    def setUp(self):
        self.title = 'Ticket title'
        self.bought = 7.56
        self.sold = 8.53
        self.profit = self.sold - self.bought
        self.today = datetime.now()
        self.user_object = User.objects.create_user(
            username='test_user',
            password='password',
        )
        self.ticket_object = Ticket.objects.create(
            user=self.user_object,
            title=self.title,
            bought=self.bought,
        )
        self.pk = self.ticket_object.pk

    def test_ticket_exists(self):
        ticket = Ticket.objects.filter(title=self.title).first()
        self.assertEqual(ticket.user, self.user_object)
        self.assertEqual(ticket.title, self.title)
        self.assertEqual(ticket.closed, 'False')
        self.assertEqual(ticket.bought, 7.56)
        self.assertIsNone(ticket.sold)
        self.assertIsNone(ticket.profit)
        self.assertIsNone(ticket.category)
        self.assertEqual(ticket.created_at.date(), self.today.date())
        self.assertEqual(ticket.closed_at.date(), self.today.date())
        self.assertEqual(ticket.deleted, 'False')
        print('SUCCESS | TestAccountingModels | test_ticket_exists')

    def test_ticket_update(self):
        ticket = Ticket.objects.filter(title=self.title).first()
        ticket.title = 'Ticket'
        ticket.sold = self.sold
        ticket.profit = self.profit
        ticket.save()
        self.assertEqual(ticket.title, 'Ticket')
        self.assertEqual(ticket.sold, self.sold)
        self.assertEqual(ticket.profit, self.profit)
        print('SUCCESS | TestAccountingModels | test_ticket_update')

    def test_get_update_url(self):
        self.assertEqual(Ticket.get_update_url(self), f'/update/{self.pk}')
        print('SUCCESS | TestAccountingModels | test_get_update_url')

    def test_get_delete_url(self):
        self.assertEqual(Ticket.get_delete_url(self), f'/delete/{self.pk}')
        print('SUCCESS | TestAccountingModels | test_get_delete_url')

    def test_str_method(self):
        self.assertEqual(Ticket.__str__(self), self.title)
        print('SUCCESS | TestAccountingModels | test_str_method')



