import pytest

from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth.models import User

from tests.conftest import created_user, client
from user.models import UserProfile, UserSettings


@pytest.mark.django_db
def test_register_correct_data(client):
    register_endpoint = reverse('register')
    response = client.post(
        register_endpoint,
        data={
            'username': 'test_user_2',
            'password1': '1e23ru0w9eriJ',
            'password2': '1e23ru0w9eriJ',
        })
    new_user = User.objects.filter(username='test_user_2').first()
    user_settings_exists = UserSettings.objects.filter(
        user=new_user,
        paginate_by__paginate_by=10,
        currency__currency='$',
        display_symbol=False,
        delete_confirmation=True,
    ).exists()
    user_profile_exists = UserProfile.objects.filter(
        user=new_user,
        all_time_profit=0,
        tickets_quantity=0,
        highest_profit=0,
        highest_loss=0,
    ).exists()
    alert_message = 'You successfully registered!'
    response_message = str(list(get_messages(response.wsgi_request))[0])

    assert user_settings_exists
    assert user_profile_exists
    assert response.status_code == 302
    assert response.url == reverse('home')
    assert alert_message in response_message


@pytest.mark.django_db
def test_register_incorrect_data(client):
    register_endpoint = reverse('register')
    response = client.post(
        register_endpoint,
        data={
            'username': 'test_user_2',
            'password1': '123',
            'password2': '798',
        })
    alert_message = 'Registration error.'
    response_message = str(list(get_messages(response.wsgi_request))[0])

    assert response.status_code == 200
    assert alert_message in response_message


@pytest.mark.django_db
def test_register_auth_user_redirected(created_user, register_user, client):
    register_endpoint = reverse('register')
    response = client.get(register_endpoint)

    assert response.status_code == 302
    assert response.url == reverse('home')


def test_register_used_template(client):
    register_endpoint = reverse('register')
    response = client.get(register_endpoint)

    assert 'user/register.html' in (template.name for template in response.templates)


