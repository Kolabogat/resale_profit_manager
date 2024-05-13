import pytest

from django.contrib.messages import get_messages
from django.urls import reverse

from tests.conftest import created_user, client, logged_user, TEST_USERNAME, TEST_PASSWORD


@pytest.mark.django_db
def test_user_login_success(
        created_user,
        client,
):
    user_login_endpoint = reverse('login')
    response = client.post(
        user_login_endpoint,
        data={
            'username': TEST_USERNAME,
            'password': TEST_PASSWORD,
        })
    alert_message = 'Welcome back User. You successfully logged in!'
    response_message = str(list(get_messages(response.wsgi_request))[0])

    assert response.status_code == 302
    assert response.url == reverse('home')
    assert alert_message in response_message


@pytest.mark.django_db
def test_user_login_error(
        created_user,
        client,
):
    user_login_endpoint = reverse('login')
    response = client.post(
        user_login_endpoint,
        data={
            'username': TEST_USERNAME,
            'password': 123,
        })
    alert_message = 'Please enter a correct username and password. Note that both fields may be case-sensitive.'
    response_message = str(list(get_messages(response.wsgi_request))[0])

    assert response.status_code == 200
    assert alert_message in response_message


@pytest.mark.django_db
def test_user_login_auth_user_redirected(
        logged_user,
        client,
):
    user_login_endpoint = reverse('login')
    response = client.get(user_login_endpoint)

    assert response.status_code == 302
    assert response.url == reverse('home')


def test_user_login_used_template(
        client,
):
    user_login_endpoint = reverse('login')
    response = client.get(user_login_endpoint)

    assert 'user/login.html' in (template.name for template in response.templates)
