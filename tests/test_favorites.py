import pytest
from rest_framework import status

from .serializers import RecipeShortInfoSerializer
from .utils import (check_bad_request, check_not_authorized,
                    check_with_validate_data)


class TestFavoritesAPI:
    url_favorites = '/api/recipes/'

    @pytest.mark.django_db(transaction=True)
    def test_add_favorite(self, user_client, recipe_another_user):
        url = f'{self.url_favorites}{recipe_another_user.pk}/favorite/'
        check_with_validate_data(
            user_client,
            'post',
            url,
            code=status.HTTP_201_CREATED,
            serializer=RecipeShortInfoSerializer
        )

    @pytest.mark.django_db(transaction=True)
    def test_add_favorite_not_autorize(self, client, recipe_another_user):
        url = f'{self.url_favorites}{recipe_another_user.pk}/favorite/'
        check_not_authorized(
            client,
            'post',
            url
        )

    @pytest.mark.django_db(transaction=True)
    def test_add_favorite_bad_request(
        self, user_client, recipe_another_user, favorite_recipe_another_user
    ):
        url = f'{self.url_favorites}{recipe_another_user.pk}/favorite/'
        check_bad_request(
            user_client,
            'post',
            url
        )

    @pytest.mark.django_db(transaction=True)
    def test_delete_favorite(
        self, user_client, recipe_another_user, favorite_recipe_another_user
    ):
        url = f'{self.url_favorites}{recipe_another_user.pk}/favorite/'
        check_with_validate_data(
            user_client,
            'delete',
            url,
            code=status.HTTP_204_NO_CONTENT
        )

    @pytest.mark.django_db(transaction=True)
    def test_delete_favorite_not_autorize(self, client, recipe_another_user):
        url = f'{self.url_favorites}{recipe_another_user.pk}/favorite/'
        check_not_authorized(
            client,
            'delete',
            url
        )

    @pytest.mark.django_db(transaction=True)
    def test_delete_favorite_bad_request(
        self, user_client, recipe_another_user
    ):
        url = f'{self.url_favorites}{recipe_another_user.pk}/favorite/'
        check_bad_request(
            user_client,
            'delete',
            url
        )
