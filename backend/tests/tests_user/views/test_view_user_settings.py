import pytest
from django.urls import reverse
from django.contrib.messages import get_messages

from user.models import UserSettings


@pytest.mark.django_db
def test_user_settings(
        logged_user,
        client,
        ticket,
):
    user_settings_endpoint = reverse('user_settings')
    response = client.get(user_settings_endpoint)

    assert response.status_code == 200
    assert response.context.get('command_currency').first().currency == '$'
    assert response.context.get('command_pagination').first().paginate_by == 5


@pytest.mark.django_db
def test_user_settings_update(
        logged_user,
        client,
        add_currency_and_pagination_values,
):
    user_settings_endpoint = reverse('user_settings')
    response = client.post(
        user_settings_endpoint,
        data={
            'paginate_by': 3,
            'currency': 2,
            'display_symbol': True,
            'delete_confirmation': False,
        })
    alert_message = 'Your settings saved.'
    response_message = str(list(get_messages(response.wsgi_request))[0])

    assert response.status_code == 302
    assert response.url == reverse('user_settings')
    assert alert_message in response_message

    updated_user_settings_exists = UserSettings.objects.filter(
        user=logged_user,
        paginate_by=3,
        currency=2,
        display_symbol=True,
        delete_confirmation=False,
    ).exists

    assert updated_user_settings_exists


@pytest.mark.django_db
def test_user_settings_used_template(
        logged_user,
        client,
):
    user_settings_endpoint = reverse('user_settings')
    response = client.get(user_settings_endpoint)

    assert 'user/user_settings.html' in (template.name for template in response.templates)
