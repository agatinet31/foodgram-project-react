import pytest
from rest_framework import status

from .serializers import SubscribeInfoListField, SubscribeInfoSerializer
from .utils import (check_bad_request, check_not_authorized,
                    check_with_validate_data)


class TestSubscriptionsAPI:
    url_users_subscriptions = '/api/users/subscriptions/'
    url_users = '/api/users/'

    @pytest.mark.django_db(transaction=True)
    def test_list_user_subscriptions(
        self, user_client, subscription_user_to_another_user
    ):
        url = self.url_users_subscriptions
        check_with_validate_data(
            user_client,
            'get',
            url,
            serializer=SubscribeInfoListField
        )

    @pytest.mark.django_db(transaction=True)
    def test_list_user_subscriptions_not_autorize(self, client):
        url = self.url_users_subscriptions
        check_not_authorized(
            client,
            'get',
            url
        )

    @pytest.mark.django_db(transaction=True)
    def test_add_user_subscriptions(self, user_client, another_user):
        url = f'{self.url_users}{another_user.pk}/subscribe/'
        check_with_validate_data(
            user_client,
            'post',
            url,
            code=status.HTTP_201_CREATED,
            serializer=SubscribeInfoSerializer
        )

    @pytest.mark.django_db(transaction=True)
    def test_add_user_subscriptions_bad(self, user_client, user):
        url = f'{self.url_users}{user.pk}/subscribe/'
        check_bad_request(
            user_client,
            'post',
            url
        )

    @pytest.mark.django_db(transaction=True)
    def test_add_user_subscriptions_not_autorized(self, client, user):
        url = f'{self.url_users}{user.pk}/subscribe/'
        check_not_authorized(
            client,
            'post',
            url
        )

    @pytest.mark.django_db(transaction=True)
    def test_add_user_subscriptions_404(self, user_client):
        url = f'{self.url_users}1000/subscribe/'
        check_bad_request(
            user_client,
            'post',
            url,
            code=status.HTTP_404_NOT_FOUND
        )

    @pytest.mark.django_db(transaction=True)
    def test_delete_user_subscriptions(
        self, user_client, another_user, subscription_user_to_another_user
    ):
        url = f'{self.url_users}{another_user.pk}/subscribe/'
        check_with_validate_data(
            user_client,
            'delete',
            url,
            code=status.HTTP_204_NO_CONTENT
        )

    @pytest.mark.django_db(transaction=True)
    def test_delete_user_subscriptions_bad(self, user_client, another_user):
        url = f'{self.url_users}{another_user.pk}/subscribe/'
        check_bad_request(
            user_client,
            'delete',
            url
        )

    @pytest.mark.django_db(transaction=True)
    def test_delete_user_subscriptions_not_autorized(self, client, user):
        url = f'{self.url_users}{user.pk}/subscribe/'
        check_not_authorized(
            client,
            'delete',
            url
        )

    @pytest.mark.django_db(transaction=True)
    def test_delete_user_subscriptions_404(self, user_client):
        url = f'{self.url_users}1000/subscribe/'
        check_bad_request(
            user_client,
            'delete',
            url,
            code=status.HTTP_404_NOT_FOUND
        )
