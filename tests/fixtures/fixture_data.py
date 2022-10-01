import tempfile

import pytest

from recipes.models import Recipe, Tag, Ingredient


@pytest.fixture
def tag1():
    return Tag.objects.create(
        name='Завтрак',
        color='#458B74',
        slug='breakfast'
    )


@pytest.fixture
def tag2():
    return Tag.objects.create(
        name='Обед',
        color='#EAEE80',
        slug='launch'
    )


@pytest.fixture
def tag3():
    return Tag.objects.create(
        name='Ужин',
        color='#DC143D',
        slug='dinner'
    )


@pytest.fixture
def ingredient_1():
    return Ingredient.objects.create(
        name='Ингридиент1',
        measurement_unit='г'
    )


@pytest.fixture
def ingredient_2():
    return Ingredient.objects.create(
        name='Ингридиент2',
        measurement_unit='кг'
    )


@pytest.fixture
def ingredient_3():
    return Ingredient.objects.create(
        name='Ингридиент2',
        measurement_unit='кг'
    )


@pytest.fixture
def recipe_user(user, another_user, ingredient_1, ingredient_2, tag1, tag2):
    recipe = Recipe.objects.create(
        name='Рецепт1',
        image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
        text='Текст рецепта1',
        cooking_time=10,
        author=user
    )
    Recipe.objects.ingredients.through.create(
        recipe=recipe,
        ingredient=ingredient_1,
        amount=1
    )
    Recipe.objects.ingredients.through.create(
        recipe=recipe,
        ingredient=ingredient_2,
        amount=2
    )
    Recipe.objects.tags.through.create(
        recipe=recipe,
        tag=tag1
    )
    Recipe.objects.tags.through.create(
        recipe=recipe,
        tag=tag2
    )
    from fixture_user import another_user
    Recipe.objects.favorites.through.create(
        recipe=recipe,
        customuser=another_user
    )
    Recipe.objects.shopping_carts.through.create(
        recipe=recipe,
        customuser=another_user
    )
    return recipe


@pytest.fixture
def recipe_another_user(another_user, ingredient_3, tag2, tag3):
    recipe = Recipe.objects.create(
        name='Рецепт2',
        image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
        text='Текст рецепта2',
        cooking_time=10,
        author=another_user
    )
    Recipe.objects.ingredients.through.create(
        recipe=recipe,
        ingredient=ingredient_3,
        amount=1
    )
    Recipe.objects.tags.through.create(
        recipe=recipe,
        tag=tag2
    )
    Recipe.objects.tags.through.create(
        recipe=recipe,
        tag=tag3
    )
    return recipe
