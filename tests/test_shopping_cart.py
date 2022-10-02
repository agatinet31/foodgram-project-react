import pytest
from rest_framework import status

from .serializers import RecipeShortInfoSerializer
from .utils import (check_bad_request, check_not_authorized,
                    check_with_validate_data)


class TestShoppingCartAPI:
    url_download_shopping_cart = '/api/recipes/download_shopping_cart/'
    url_recipes = '/api/recipes/'

    @pytest.mark.django_db(transaction=True)
    def test_download_shopping_cart_ok(self, user_client, recipe_user):
        url = self.url_download_shopping_cart
        check_with_validate_data(
            user_client,
            'get',
            url
        )

    @pytest.mark.django_db(transaction=True)
    def test_download_shopping_cart_not_authorized(
        self, client, recipe_another_user
    ):
        url = self.url_download_shopping_cart
        check_not_authorized(
            client,
            'get',
            url
        )

    @pytest.mark.django_db(transaction=True)
    def test_add_shopping_cart(
        self, user_client, recipe_another_user
    ):
        url = f'{self.url_recipes}{recipe_another_user.pk}/shopping_cart/'
        check_with_validate_data(
            user_client,
            'post',
            url,
            code=status.HTTP_201_CREATED,
            serializer=RecipeShortInfoSerializer
        )

    @pytest.mark.django_db(transaction=True)
    def test_add_shopping_cart_bad_request(
        self, user_client, recipe_user
    ):
        url = f'{self.url_recipes}{recipe_user.pk}/shopping_cart/'
        check_bad_request(
            user_client,
            'post',
            url
        )

    @pytest.mark.django_db(transaction=True)
    def test_add_shopping_cart_not_autorize(self, client, recipe_another_user):
        url = f'{self.url_recipes}{recipe_another_user.pk}/shopping_cart/'
        check_not_authorized(
            client,
            'post',
            url
        )

    @pytest.mark.django_db(transaction=True)
    def test_delete_shopping_cart(
        self, user_client, recipe_user
    ):
        url = f'{self.url_recipes}{recipe_user.pk}/shopping_cart/'
        check_with_validate_data(
            user_client,
            'delete',
            url,
            code=status.HTTP_204_NO_CONTENT
        )

    @pytest.mark.django_db(transaction=True)
    def test_delete_shopping_cart_not_autorize(
        self, client, recipe_another_user
    ):
        url = f'{self.url_recipes}{recipe_another_user.pk}/shopping_cart/'
        check_not_authorized(
            client,
            'delete',
            url
        )

    @pytest.mark.django_db(transaction=True)
    def test_delete_shopping_cart_bad_request(
        self, user_client, recipe_another_user
    ):
        url = f'{self.url_recipes}{recipe_another_user.pk}/shopping_cart/'
        check_bad_request(
            user_client,
            'delete',
            url
        )
