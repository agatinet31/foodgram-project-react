from time import process_time_ns
import pytest
from rest_framework import status

from .serializers import (RecipeShortInfoSerializer, RecipesResponseListField,
                          RecipesResponseSerializer, RecipesRequestSerializer, RecipesRequestSerializer)
from .utils import (check_bad_request, check_not_authorized,
                    check_with_validate_data)


class TestRecipesAPI:
    url_recipes = '/api/recipes/'

    @pytest.mark.django_db(transaction=True)
    def test_list_recipes(self, client, recipe_user, recipe_another_user):
        url = self.url_recipes
        check_with_validate_data(
            client,
            'get',
            url,
            pagination=True,
            serializer=RecipesResponseListField
        )

    @pytest.mark.django_db(transaction=True)
    def test_get_recipe(self, client, recipe_another_user):
        url = f'{self.url_recipes}{recipe_another_user.pk}/'
        check_with_validate_data(
            client,
            'get',
            url,
            serializer=RecipesResponseSerializer
        )

    @pytest.mark.django_db(transaction=True)
    def test_delete_recipe(
        self, user_client, recipe_user
    ):
        url = f'{self.url_recipes}{recipe_user.pk}/'
        check_with_validate_data(
            user_client,
            'delete',
            url,
            code=status.HTTP_204_NO_CONTENT
        )

    @pytest.mark.django_db(transaction=True)
    def test_delete_recipe_not_autorize(self, client, recipe_user):
        url = f'{self.url_recipes}{recipe_user.pk}/'
        check_not_authorized(
            client,
            'delete',
            url
        )

    @pytest.mark.django_db(transaction=True)
    def test_delete_recipe_bad_request_403(
        self, user_client, recipe_another_user
    ):
        url = f'{self.url_recipes}{recipe_another_user.pk}/'
        check_bad_request(
            user_client,
            'delete',
            url,
            code=status.HTTP_403_FORBIDDEN
        )

    @pytest.mark.django_db(transaction=True)
    def test_delete_recipe_bad_request_404(
        self, user_client, recipe_another_user
    ):
        url = f'{self.url_recipes}1000/'
        check_bad_request(
            user_client,
            'delete',
            url,
            code=status.HTTP_404_NOT_FOUND
        )

    @pytest.mark.django_db(transaction=True)
    def test_create_recipe(
        self, user_client, user,
        ingredient_1, ingredient_2, ingredient_3, tag1, tag2
    ):
        url = self.url_recipes
        data = {
            'name': 'string',
            'text': 'string',
            'cooking_time': 1,
            'ingredients': [
                {'id': 1, 'amount': 1},
                {'id': 2, 'amount': 2},
                {'id': 3, 'amount': 3},
            ],
            'tags': [
                1,
                2
            ],
            'image': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAA'
            'AEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWX'
            'MAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAA'
            'AAggCByxOyYQAAAABJRU5ErkJggg==',
        }
        check_with_validate_data(
            user_client,
            'post',
            url,
            data=data,
            code=status.HTTP_201_CREATED,
            serializer=RecipesResponseSerializer
        )

    @pytest.mark.django_db(transaction=True)
    def test_create_recipe_bad_request_400(
        self, user_client, ingredient_1, tag1
    ):
        url = self.url_recipes
        data = {
            'name': 'string',
            'text': 'string',
            'cooking_time': 1,
            'ingredients_test': [
                {'id': 1, 'amount': 1},
            ],
            'tags_qwerty': [
                1
            ],
            'image': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAA'
            'AEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWX'
            'MAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAA'
            'AAggCByxOyYQAAAABJRU5ErkJggg==',
        }
        check_bad_request(
            user_client,
            'post',
            url,
            data=data
        )

    @pytest.mark.django_db(transaction=True)
    def test_create_recipe_not_authorized(self, client):
        url = self.url_recipes
        check_not_authorized(
            client,
            'post',
            url
        )

    @pytest.mark.django_db(transaction=True)
    def test_create_recipe_bad_request_404(
        self, user_client, ingredient_1, tag1
    ):
        url = self.url_recipes
        data = {
            'name': 'string',
            'text': 'string',
            'cooking_time': 1,
            'ingredients': [
                {'id': 1, 'amount': 1},
                {'id': 2, 'amount': 2},
                {'id': 3, 'amount': 3},
            ],
            'tags': [
                1,
                2
            ],
            'image': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAA'
            'AEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWX'
            'MAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAA'
            'AAggCByxOyYQAAAABJRU5ErkJggg==',
        }
        check_bad_request(
            user_client,
            'post',
            url,
            data=data,
            code=status.HTTP_404_NOT_FOUND
        )

    @pytest.mark.django_db(transaction=True)
    def test_patch_recipe(self, user_client, recipe_user, user, ingredient_1, ingredient_2, tag1, tag2):
        url = f'{self.url_recipes}{recipe_user.pk}/'
        data = {
            'ingredients': [{'id': 1, 'amount': 10}],
            'tags': [1],
            'image': "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
            'name': "string",
            'text': "string",
            'cooking_time': 1
        }
        # data = RecipesRequestSerializer(instance=recipe_user).data
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(data)
        print('$$$$$$$$$$$$$$$$$$$')
        print(ingredient_1.pk)
        check_with_validate_data(
            user_client,
            'patch',
            url,
            data=data,
            code=status.HTTP_201_CREATED,
            # serializer=RecipesResponseSerializer
        )

    @pytest.mark.django_db(transaction=True)
    def test_patch_recipe_bad_request_400(self, user_client, recipe_user):
        url = f'{self.url_recipes}{recipe_user.pk}/'
        check_bad_request(
            user_client,
            'patch',
            url
        )

    @pytest.mark.django_db(transaction=True)
    def test_patch_recipe_not_authorized(self, client, recipe_user):
        url = f'{self.url_recipes}{recipe_user.pk}/'
        check_not_authorized(
            client,
            'patch',
            url
        )

    @pytest.mark.django_db(transaction=True)
    def test_patch_recipe_bad_request_404(self, user_client, recipe_user):
        url = f'{self.url_recipes}{recipe_user.pk}/'
        data={
            
        }
        check_bad_request(
            user_client,
            'patch',
            url,
            data=data,
            code=status.HTTP_404_NOT_FOUND
        )
