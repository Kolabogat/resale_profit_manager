import pytest
from tests.conftest import user
from user.models import UserSettings, CommandPagination, CommandCurrency


@pytest.mark.django_db
def test_model_command_currency_str_method(user):
    currency_object = CommandCurrency.objects.filter(pk=1).first()

    assert currency_object.currency == '$'


@pytest.mark.django_db
def test_model_command_pagination_str_method(user):
    pagination_object = CommandPagination.objects.filter(pk=2).first()

    assert pagination_object.paginate_by == 10


@pytest.mark.django_db
def test_model_user_settings_fields(user):
    user_settings_exists = UserSettings.objects.filter(
        user=user,
        paginate_by=2,
        currency=1,
        display_symbol=False,
        delete_confirmation=True,
    ).exists()

    assert user_settings_exists


@pytest.mark.django_db
def test_model_user_profile_str_method(user):
    user_settings = UserSettings.objects.filter(
        user=user,
        paginate_by=2,
        currency=1,
        display_symbol=False,
        delete_confirmation=True,
    ).first()
    str_method = UserSettings.__str__(user_settings)

    assert str_method == user.username
