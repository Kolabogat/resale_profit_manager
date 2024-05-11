# from django.db.models import Q
# from django.test import TestCase, Client
# from django.contrib.auth.models import User
#
# import random
# from backend.settings import FILTER_TICKETS
# from accounting.models import Ticket, TicketFilter
# from datetime import datetime
# from django.urls import reverse
# from user.models import UserProfile, UserSettings
#
#
# class TestTicketModels(TestCase):
#     def setUp(self):
#         self.bought = 7.56
#         self.sold = 8.53
#         self.profit = self.sold - self.bought
#         self.today = datetime.now()
#         self.user_object = User.objects.create_user(
#             username='test_user',
#             password='password',
#         )
#         self.ticket_object = Ticket.objects.create(
#             user=self.user_object,
#             title='Ticket title',
#             bought=self.bought,
#         )
#
#     def test_ticket_exists(self):
#         ticket = Ticket.objects.filter(title=self.ticket_object.title).first()
#         self.assertEqual(ticket.user, self.user_object)
#         self.assertEqual(ticket.title, self.ticket_object.title)
#         self.assertEqual(ticket.closed, 'False')
#         self.assertEqual(ticket.bought, 7.56)
#         self.assertIsNone(ticket.sold)
#         self.assertIsNone(ticket.profit)
#         self.assertIsNone(ticket.category)
#         self.assertEqual(ticket.created_at.date(), self.today.date())
#         self.assertEqual(ticket.closed_at.date(), self.today.date())
#         self.assertEqual(ticket.deleted, 'False')
#
#     def test_ticket_update(self):
#         ticket = Ticket.objects.filter(title=self.ticket_object.title).first()
#         ticket.title = 'Ticket'
#         ticket.sold = self.sold
#         ticket.profit = self.profit
#         ticket.save()
#         self.assertEqual(ticket.title, 'Ticket')
#         self.assertEqual(ticket.sold, self.sold)
#         self.assertEqual(ticket.profit, self.profit)
#
#     def test_get_update_url(self):
#         self.assertEqual(Ticket.get_update_url(self.ticket_object), f'/update/{self.ticket_object.pk}')
#
#     def test_get_delete_url(self):
#         self.assertEqual(Ticket.get_delete_url(self.ticket_object), f'/delete/{self.ticket_object.pk}')
#
#     def test_str_method(self):
#         self.assertEqual(Ticket.__str__(self.ticket_object), self.ticket_object.title)
#
#
# class TestTicketFilterModel(TestCase):
#     def setUp(self):
#         for filter_dict in FILTER_TICKETS:
#             filter_model = TicketFilter(**filter_dict)
#             filter_model.save()
#
#     def test_ticket_filter(self):
#         for filter_dict in FILTER_TICKETS:
#             ticket_filter = TicketFilter.objects.filter(**filter_dict).first()
#             self.assertEqual(ticket_filter.pk, filter_dict.get('pk'))
#             self.assertEqual(ticket_filter.title, filter_dict.get('title'))
#             self.assertEqual(ticket_filter.url_value, filter_dict.get('url_value'))
#             self.assertEqual(ticket_filter.annotation, filter_dict.get('annotation'))
#             self.assertEqual(ticket_filter.color, filter_dict.get('color'))
#
#
# class TestTicketViews(TestCase):
#     def setUp(self):
#         for filter_dict in FILTER_TICKETS:
#             filter_model = TicketFilter(**filter_dict)
#             filter_model.save()
#         self.client = Client()
#         self.user = User.objects.create_user(
#             username='test_user',
#             password='password',
#         )
#         self.user_profile = UserProfile.objects.create(
#             user=self.user,
#         )
#         self.user_settings = UserSettings.objects.create(
#             user=self.user,
#         )
#         for number in range(1, 6):
#             bought = random.randrange(1, 50)
#             sold = random.randrange(10, 60)
#             profit = sold - bought
#             Ticket.objects.create(
#                 user=self.user,
#                 title=f'Ticket {number}',
#                 bought=bought,
#                 sold=sold,
#                 profit=profit,
#             )
#         self.uncompleted_ticket = Ticket.objects.create(
#             user=self.user,
#             title='Uncompleted ticket',
#             bought=3.68,
#         )
#         self.q = Q(user=self.user) & Q(deleted=False)
#         self.client.login(username='test_user', password='password')
#
#         self.home = reverse('home')
#         self.add_ticket = reverse('add_ticket')
#         self.update_ticket = reverse('update_ticket', args=[self.uncompleted_ticket.pk])
#         self.delete_ticket = reverse('delete_ticket', args=[self.uncompleted_ticket.pk])
#
#     def test_view_tickets_GET(self):
#         response = self.client.get(self.home)
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'Ticket 1')
#
#     def test_add_ticket_uncompleted_POST(self):
#         response = self.client.post(self.add_ticket, data={
#             'title': 'Ticket 12',
#             'bought': 3.68,
#         })
#         new_ticket = Ticket.objects.filter(
#             title='Ticket 12',
#             bought=3.68,
#             sold=None,
#             profit=None,
#         ).first()
#         self.assertIsNotNone(new_ticket)
#         self.assertEqual(response.status_code, 302)
#
#     def test_add_ticket_completed_POST(self):
#         response = self.client.post(self.add_ticket, data={
#             'title': 'Ticket 12',
#             'bought': 3.68,
#             'sold': 4.23,
#         })
#         new_ticket = Ticket.objects.filter(
#             title='Ticket 12',
#             bought=3.68,
#             sold=4.23,
#             profit=0.55,
#         ).first()
#         self.assertIsNotNone(new_ticket)
#         self.assertEqual(response.status_code, 302)
#
#     def test_update_ticket_profit_plus_POST(self):
#         response = self.client.post(self.update_ticket, data={
#             'title': 'Updated ticket',
#             'bought': 3.68,
#             'sold': 7.12,
#         })
#         updated_ticket = Ticket.objects.filter(
#             title='Updated ticket',
#             bought=3.68,
#             sold=7.12,
#             profit=3.44,
#         ).first()
#         self.assertIsNotNone(updated_ticket)
#         self.assertEqual(response.status_code, 302)
#
#     def test_update_ticket_profit_minus_POST(self):
#         response = self.client.post(self.update_ticket, data={
#             'title': 'Updated ticket',
#             'bought': 3.68,
#             'sold': 2.12,
#         })
#         updated_ticket = Ticket.objects.filter(
#             title='Updated ticket',
#             bought=3.68,
#             sold=2.12,
#             profit=-1.56,
#         ).first()
#         self.assertIsNotNone(updated_ticket)
#         self.assertEqual(response.status_code, 302)
#
#     def test_delete_ticket_DELETE(self):
#         response = self.client.delete(self.delete_ticket)
#         deleted_ticket = Ticket.objects.filter(
#             title=self.uncompleted_ticket.title,
#             bought=self.uncompleted_ticket.bought,
#             deleted=True,
#         )
#         self.assertIsNotNone(deleted_ticket)
#         self.assertEqual(response.status_code, 302)
#
#     def test_filter_profit_waiting_GET(self):
#         response = self.client.get('?filter_by=profit_waiting', follow=True)
#         q = self.q & Q(profit=None)
#         profit_waiting = Ticket.objects.filter(q)
#         other_tickets = Ticket.objects.filter(~q)
#
#         for ticket in profit_waiting:
#             self.assertContains(response, ticket.title)
#         for ticket in other_tickets:
#             self.assertNotContains(response, ticket.title)
#         self.assertEqual(response.status_code, 200)
#
#     def test_filter_profit_failure_GET(self):
#         response = self.client.get('?filter_by=profit_failure', follow=True)
#         q = self.q & Q(profit__lt=0)
#         profit_failure = Ticket.objects.filter(q)
#         other_tickets = Ticket.objects.filter(~q)
#
#         for ticket in profit_failure:
#             self.assertContains(response, ticket.title)
#         for ticket in other_tickets:
#             self.assertNotContains(response, ticket.title)
#         self.assertEqual(response.status_code, 200)
#
#     def test_filter_profit_nothing_GET(self):
#         response = self.client.get('?filter_by=profit_nothing', follow=True)
#         q = self.q & Q(profit=0)
#         profit_nothing = Ticket.objects.filter(q)
#         other_tickets = Ticket.objects.filter(~q)
#
#         for ticket in profit_nothing:
#             self.assertContains(response, ticket.title)
#         for ticket in other_tickets:
#             self.assertNotContains(response, ticket.title)
#         self.assertEqual(response.status_code, 200)
#
#     def test_filter_profit_success_GET(self):
#         response = self.client.get('?filter_by=profit_success', follow=True)
#         q = self.q & Q(profit__gt=0)
#         profit_success = Ticket.objects.filter(q)
#         other_tickets = Ticket.objects.filter(~q)
#
#         for ticket in profit_success:
#             self.assertContains(response, ticket.title)
#         for ticket in other_tickets:
#             self.assertNotContains(response, ticket.title)
#         self.assertEqual(response.status_code, 200)
