import pytest
from tests.conftest import user
from django.contrib.auth.models import User

from user.models import UserSettings, UserProfile
from tests.conftest import TEST_USERNAME, TEST_PASSWORD, TEST_EMAIL


@pytest.mark.django_db
def test_user_and_additional_models_created(user):
    user_object = User.objects.filter(
        username=TEST_USERNAME,
        email=TEST_EMAIL,
    ).first()
    settings_user = UserSettings.objects.filter(
        user=user_object.pk
    ).first()
    profile_user = UserProfile.objects.filter(
        user=user_object.pk
    ).first()
    user_objects = User.objects.all()
    profile_users = UserProfile.objects.all()

    assert user_object in user_objects
    assert settings_user.paginate_by.paginate_by == 10
    assert settings_user.currency.currency == '$'
    assert not settings_user.display_symbol  # False
    assert settings_user.delete_confirmation  # True
    assert profile_user in profile_users
