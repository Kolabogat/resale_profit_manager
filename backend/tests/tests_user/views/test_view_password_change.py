import pytest
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password


@pytest.mark.django_db
def test_password_change_correct_data(
        logged_user,
        client,
):
    new_password = 'strong123pass974H'
    password_change_endpoint = reverse('password_change')
    response = client.post(
        password_change_endpoint,
        data={
            'new_password1': new_password,
            'new_password2': new_password,
        })
    updated_user = User.objects.filter(username=logged_user.username).first()
    alert_message = 'Your password has been successfully changed.'
    response_message = str(list(get_messages(response.wsgi_request))[0])

    assert check_password(new_password, updated_user.password)
    assert response.status_code == 302
    assert alert_message in response_message


@pytest.mark.django_db
def test_password_change_incorrect_data(
        logged_user,
        client,
):
    new_password = 'strong123pass974H'
    password_change_endpoint = reverse('password_change')
    response = client.post(
        password_change_endpoint,
        data={
            'new_password1': new_password,
            'new_password2': 'str123',
        })
    alert_message = 'The two password fields didn’t match.'
    response_message = str(list(get_messages(response.wsgi_request))[0])

    assert response.status_code == 200
    assert alert_message in response_message


@pytest.mark.django_db
def test_password_change_used_template(
        logged_user,
        client,
):
    password_change_endpoint = reverse('password_change')
    response = client.get(password_change_endpoint)

    assert 'user/password_change.html' in (template.name for template in response.templates)