from django.test import TestCase, Client
from django.contrib.auth.models import User

from accounting.management.commands.command_filter_query import FILTER_TICKETS
from accounting.models import TicketFilter, Ticket
from user.models import UserSettings, UserProfile
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password


class TestUserModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            password='password',
        )

    def test_user_settings(self):
        """
        Check that additional model 'UserSettings' for User
        created correctly
        """
        user_settings = UserSettings.objects.create(
            user=self.user
        )
        self.assertEqual(user_settings.user, self.user)
        self.assertEqual(user_settings.paginate_by.paginate_by, 10)
        self.assertEqual(user_settings.currency.currency, '$')
        self.assertFalse(user_settings.display_symbol)
        self.assertTrue(user_settings.delete_confirmation)

    def test_user_profile(self):
        """
        Check that additional model 'UserProfile' for User
        created correctly
        """
        user_profile = UserProfile.objects.create(
            user=self.user
        )
        self.assertEqual(user_profile.user, self.user)
        self.assertEqual(user_profile.all_time_profit, 0)
        self.assertEqual(user_profile.tickets_quantity, 0)
        self.assertEqual(user_profile.highest_profit, 0)
        self.assertEqual(user_profile.highest_loss, 0)


class TestUserViews(TestCase):
    def setUp(self):
        """
        Setup: TicketFilter, Client, User, UserProfile,
        UserSettings, Ticket, login user, urls.
        """
        for filter_dict in FILTER_TICKETS:
            filter_model = TicketFilter(**filter_dict)
            filter_model.save()
        self.client = Client()
        self.user = User.objects.create_user(
            username='test_user',
            password='password',
        )
        self.user_profile = UserProfile.objects.create(
            user=self.user,
        )
        self.user_settings = UserSettings.objects.create(
            user=self.user,
        )
        self.ticket = Ticket.objects.create(
            user=self.user,
            title='Ticket title',
            bought=6.23,
            sold=7.54,
            profit=7.54-6.23,
        )
        self.client.login(username='test_user', password='password')

        self.register = reverse('register')
        self.login = reverse('login')
        self.logout = reverse('logout')
        self.password_change = reverse('password_change')
        self.account_profile = reverse('account_profile')
        self.update_profile = reverse('update_profile')
        self.user_settings = reverse('user_settings')

    def test_register_POST(self):
        """
        Test register view
        Create: register new user
        Check: additional models for user created
        correctly; status code; used template.
        """
        self.client.logout()
        response = self.client.post(self.register, data={
            'username': 'test_user_2',
            'password1': '1e23ru0w9eriJ',
            'password2': '1e23ru0w9eriJ',
        })
        registered_user = User.objects.filter(username='test_user_2').first()
        settings_user = UserSettings.objects.filter(user=registered_user).first()
        profile_user = UserProfile.objects.filter(user=registered_user).first()
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('user/register.html')
        self.assertEqual(registered_user.username, 'test_user_2')
        self.assertEqual(settings_user.paginate_by.paginate_by, 10)
        self.assertEqual(settings_user.currency.currency, '$')
        self.assertFalse(settings_user.display_symbol)
        self.assertTrue(settings_user.delete_confirmation)
        self.assertEqual(profile_user.all_time_profit, 0)

    def test_register_not_allowed_for_auth_user_GET(self):
        """
        Test register view
        Check: registration template,
        not available for logged-in user,
        instead user redirected to home page;
        status code.
        """
        response = self.client.get(self.register)
        self.assertEqual(response.status_code, 302)

    def test_login_POST(self):
        """
        Test login view
        Check: login work correctly;
        status code; used template.
        """
        self.client.logout()
        response = self.client.post(self.login, data={
            'username': 'test_user',
            'password': 'password',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('user/login.html')

    def test_login_not_allowed_for_auth_user_GET(self):
        """
        Test login view
        Check: login template,
        not available for logged-in user,
        instead user redirected to home page;
        status code.
        """
        response = self.client.get(self.login)
        self.assertEqual(response.status_code, 302)

    def test_logout_GET(self):
        """
        Test logout view
        Check: user logout and redirected
        to login page; status code; redirect
        """
        response = self.client.get(self.logout, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[-1][-1], 302)
        self.assertEqual(response.resolver_match.url_name, 'login')

    def test_password_change_success_POST(self):
        """
        Test password_change view
        Check: password changed correctly;
        status code; used template
        """
        response = self.client.post(self.password_change, data={
            'new_password1': 'strong123pass974H',
            'new_password2': 'strong123pass974H',
        })
        changed_user = User.objects.filter(username=self.user.username).first()
        self.assertTrue(check_password('strong123pass974H', changed_user.password))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('user/password_change.html')

    def test_password_change_error_short_password_POST(self):
        """
        Test password_change view
        Check: error "password is too short" appeared;
        status code
        """
        response = self.client.post(self.password_change, follow=True, data={
            'new_password1': '123',
            'new_password2': '123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This password is too short. It must contain at least 8 characters.')
        self.assertEqual(response.redirect_chain, [])
        self.assertEqual(response.resolver_match.url_name, 'password_change')

    def test_password_change_error_no_match_POST(self):
        """
        Test password_change view
        Check: that error "fields didn’t match" appeared;
        status code
        """
        second_response = self.client.post(self.password_change, follow=True, data={
            'new_password1': '1342154',
            'new_password2': '123',
        })
        self.assertContains(second_response, 'The two password fields didn’t match.')

    def test_password_change_error_one_field_POST(self):
        """
        Test password_change view
        Check: that error "field is required" appeared;
        status code
        """
        third_response = self.client.post(self.password_change, follow=True, data={
            'new_password1': '1342154',
        })
        self.assertContains(third_response, 'This field is required.')

    def test_account_profile_GET(self):
        """
        Test view_user_data view
        Check: status code; used template
        """
        response = self.client.get(self.account_profile)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/account_profile.html')

    def test_update_profile_GET(self):
        """
        Test update_user_data view
        Check: profile updated correctly;
        status code; redirect
        """
        response = self.client.get(self.update_profile, follow=True)

        user_profile = UserProfile.objects.filter(user=self.user.pk).first()
        self.assertEqual(user_profile.highest_profit, 1.31)
        self.assertEqual(user_profile.highest_loss, 0)
        self.assertEqual(user_profile.all_time_profit, 1.31)
        self.assertEqual(user_profile.tickets_quantity, 1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[-1][-1], 302)
        self.assertEqual(response.resolver_match.url_name, 'account_profile')

    def test_update_profile_with_two_tickets_GET(self):
        """
        Test update_user_data view
        Check: profile updated correctly;
        status code; redirect
        """
        Ticket.objects.create(
            user=self.user,
            title='Ticket title',
            bought=12.23,
            sold=6.12,
            profit=6.12-12.23,
        )
        self.client.get(self.update_profile, follow=True)
        user_profile = UserProfile.objects.filter(user=self.user.pk).first()
        self.assertEqual(user_profile.highest_profit, 1.31)
        self.assertEqual(user_profile.highest_loss, -6.11)
        self.assertEqual(user_profile.all_time_profit, -4.8)
        self.assertEqual(user_profile.tickets_quantity, 2)

    def test_user_settings_GET(self):
        """
        Test update_user_data view
        Check: status code; used template
        """
        response = self.client.get(self.user_settings)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/user_settings.html')
