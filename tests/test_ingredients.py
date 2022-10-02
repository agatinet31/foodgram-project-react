import pytest

from .serializers import IngredientListField, IngredientSerializer
from .utils import check_with_validate_data


class TestIngredintsAPI:
    url_ingredients = '/api/ingredients/'

    @pytest.mark.django_db(transaction=True)
    def test_list_ingredients(self, client, ingredient_1, ingredient_2):
        check_with_validate_data(
            client,
            'get',
            self.url_ingredients,
            serializer=IngredientListField
        )

    @pytest.mark.django_db(transaction=True)
    def test_get_ingredient(self, client, ingredient_1):
        url = f'{self.url_ingredients}{ingredient_1.pk}/'
        check_with_validate_data(
            client,
            'get',
            url,
            serializer=IngredientSerializer
        )
