import pytest
from tests.conftest import user
from django.contrib.auth.models import User

from user.models import UserSettings, UserProfile


@pytest.mark.django_db
def test_user_and_additional_models_created(user):
    user = User.objects.filter(
        username='user',
        email='user@user.com',
    ).first()
    settings_user = UserSettings.objects.filter(
        user=user.pk
    ).first()
    profile_user = UserProfile.objects.filter(
        user=user.pk
    ).first()
    users = User.objects.all()
    profile_users = UserProfile.objects.all()

    assert user in users
    assert settings_user.paginate_by.paginate_by == 10
    assert settings_user.currency.currency == '$'
    assert not settings_user.display_symbol
    assert settings_user.delete_confirmation
    assert profile_user in profile_users
