from django.contrib.auth.models import User
import pytest
from accounting.models import Ticket
from user.models import UserSettings, UserProfile


@pytest.fixture
# @pytest.mark.django_db
def user():
    user = User.objects.create_user(
        username='user',
        email='user@user.com',
        password='a9Jd2o9gLe2axs',
    )
    settings_user = UserSettings()
    settings_user.user = user
    settings_user.save()

    profile_user = UserProfile()
    profile_user.user = user
    profile_user.save()
    return user
