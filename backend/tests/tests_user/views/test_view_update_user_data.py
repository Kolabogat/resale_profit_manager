import pytest

from django.urls import reverse
from django.contrib.messages import get_messages

from user.models import UserProfile


@pytest.mark.django_db
def test_update_user_data_with_ticket(
        logged_user,
        client,
        add_all_tickets,
        get_updated_user_profile
):
    update_user_data_endpoint = reverse('update_profile')
    response = client.get(update_user_data_endpoint)
    alert_message = 'You successfully updated your data.'
    response_message = str(list(get_messages(response.wsgi_request))[0])

    assert response.status_code == 302
    assert response.url == reverse('account_profile')
    assert alert_message in response_message

    user_profile_exists = UserProfile.objects.filter(
        user=logged_user,
        all_time_profit=get_updated_user_profile.get('all_time_profit'),
        tickets_quantity=get_updated_user_profile.get('tickets_quantity'),
        highest_profit=get_updated_user_profile.get('highest_profit'),
        highest_loss=get_updated_user_profile.get('highest_loss'),
    ).exists()

    assert user_profile_exists


@pytest.mark.django_db
def test_update_user_data_without_ticket(
        logged_user,
        client
):
    update_user_data_endpoint = reverse('update_profile')
    response = client.get(update_user_data_endpoint)
    alert_message = 'You don\'t have any tickets.'
    response_message = str(list(get_messages(response.wsgi_request))[0])

    assert response.status_code == 302
    assert response.url == reverse('account_profile')
    assert alert_message in response_message
