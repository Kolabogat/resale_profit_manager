import pytest

from django.urls import reverse

from tests.conftest import logged_user, client


@pytest.mark.django_db
def test_user_logout(
        logged_user,
        client
):
    user_logout_endpoint = reverse('logout')
    response = client.get(user_logout_endpoint)

    assert response.status_code == 302
    assert response.url == reverse('login')


@pytest.mark.django_db
def test_logout_not_auth_user_redirected(
        client
):
    user_logout_endpoint = reverse('logout')
    response = client.get(user_logout_endpoint)

    assert response.status_code == 302
    assert response.url == reverse('login')
