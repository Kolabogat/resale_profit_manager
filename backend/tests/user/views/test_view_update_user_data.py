import pytest

from django.urls import reverse
from django.contrib.messages import get_messages

from tests.conftest import created_user, client
from tests.user.conftest import get_updated_user_profile
from user.models import UserProfile


@pytest.mark.django_db
def test_update_user_data_with_ticket(created_user, login_user, client, ticket, ticket_success, ticket_failure):
    update_user_data_endpoint = reverse('update_profile')
    response = client.get(update_user_data_endpoint)
    alert_message = 'You successfully updated your data.'
    response_message = str(list(get_messages(response.wsgi_request))[0])

    assert response.status_code == 302
    assert response.url == reverse('account_profile')
    assert alert_message in response_message

    updated_profile = get_updated_user_profile(created_user)

    user_profile_exists = UserProfile.objects.filter(
        user=created_user,
        all_time_profit=updated_profile.get('all_time_profit'),
        tickets_quantity=updated_profile.get('tickets_quantity'),
        highest_profit=updated_profile.get('highest_profit'),
        highest_loss=updated_profile.get('highest_loss'),
    ).exists()

    assert user_profile_exists


@pytest.mark.django_db
def test_update_user_data_without_ticket(created_user, login_user, client):
    update_user_data_endpoint = reverse('update_profile')
    response = client.get(update_user_data_endpoint)
    alert_message = 'You don\'t have any tickets.'
    response_message = str(list(get_messages(response.wsgi_request))[0])

    assert response.status_code == 302
    assert response.url == reverse('account_profile')
    assert alert_message in response_message
