import pytest

from tests.conftest import created_user
from user.models import UserProfile


@pytest.mark.django_db
def test_model_user_profile_fields(
        created_user
):
    user_profile_exists = UserProfile.objects.filter(
        user=created_user,
        all_time_profit=0,
        tickets_quantity=0,
        highest_profit=0,
        highest_loss=0,
    ).exists()

    assert user_profile_exists


@pytest.mark.django_db
def test_model_user_profile_str_method(
        created_user
):
    user_profile = UserProfile.objects.filter(
        user=created_user,
        all_time_profit=0,
        tickets_quantity=0,
        highest_profit=0,
        highest_loss=0,
    ).first()
    str_method = UserProfile.__str__(user_profile)

    assert str_method == created_user.username
