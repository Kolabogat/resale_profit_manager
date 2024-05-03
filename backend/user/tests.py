from django.test import TestCase, Client
from django.contrib.auth.models import User
from user.models import UserSettings, UserProfile


class TestUserModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user', password='password'
        )

    def test_user_settings(self):
        user_settings = UserSettings.objects.create(
            user=self.user
        )
        self.assertEqual(user_settings.user, self.user)
        self.assertEqual(user_settings.paginate_by.paginate_by, 10)
        self.assertEqual(user_settings.currency.currency, '$')
        self.assertFalse(user_settings.display_symbol)
        self.assertTrue(user_settings.delete_confirmation)
        print('SUCCESS | TestUserModels | test_user_settings')

    def test_user_profile(self):
        user_profile = UserProfile.objects.create(
            user=self.user
        )
        self.assertEqual(user_profile.user, self.user)
        self.assertEqual(user_profile.all_time_profit, 0)
        self.assertEqual(user_profile.tickets_quantity, 0)
        self.assertEqual(user_profile.highest_profit, 0)
        self.assertEqual(user_profile.highest_loss, 0)
        print('SUCCESS | TestUserModels | test_user_profile')
