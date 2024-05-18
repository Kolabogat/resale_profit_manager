import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_view_user_data(logged_user, client):
    view_user_data_endpoint = reverse('account_profile')
    response = client.get(view_user_data_endpoint)
    user_profile = response.context.get('user_object')

    assert response.status_code == 200
    assert user_profile.all_time_profit == 0
    assert user_profile.tickets_quantity == 0
    assert user_profile.highest_profit == 0
    assert user_profile.highest_loss == 0


@pytest.mark.django_db
def test_view_user_data_updated(
        logged_user,
        client,
        add_all_tickets,
        get_updated_user_profile,
):
    update_user_data_endpoint = reverse('update_profile')
    client.get(update_user_data_endpoint)

    view_user_data_endpoint = reverse('account_profile')
    response = client.get(view_user_data_endpoint)
    context_profile = response.context.get('user_object')

    assert response.status_code == 200
    assert context_profile.all_time_profit == get_updated_user_profile.get('all_time_profit')
    assert context_profile.tickets_quantity == get_updated_user_profile.get('tickets_quantity')
    assert context_profile.highest_profit == get_updated_user_profile.get('highest_profit')
    assert context_profile.highest_loss == get_updated_user_profile.get('highest_loss')


@pytest.mark.django_db
def test_view_user_data_used_template(
        logged_user,
        client,
):
    view_user_data_endpoint = reverse('account_profile')
    response = client.get(view_user_data_endpoint)

    assert 'user/account_profile.html' in (template.name for template in response.templates)
