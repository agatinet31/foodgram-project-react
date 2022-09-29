from django.contrib.auth import get_user_model
from django.db import DatabaseError, IntegrityError, transaction
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from users.models import CustomUser, Subscriber

# from rest_framework.exceptions import ValidationError
# from rest_framework.generics import get_object_or_404

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """Сериализатор данных пользователя."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('is_subscribed',)

    def get_is_subscribed(self, author):
        """Проверка наличия подписок у пользователя."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.is_subscribed(author)


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов."""
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингридиентов."""
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeShortInfoSerializer(serializers.ModelSerializer):
    """Сериализатор с краткой информацией рецепта."""
    image = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )

    def get_image(self, obj):
        """Возвращает абсолютный URL картинки."""
        return self.context['request'].build_absolute_uri(obj.image.url)


class SubscribeParamsSerializer(serializers.Serializer):
    """Сериализатор query параметров для подписок на пользователей."""
    recipes_limit = serializers.IntegerField(required=False, min_value=1)


class SubscribeInfoSerializer(CustomUserSerializer):
    """Сериализатор информации по подпискам пользователей."""
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(CustomUserSerializer.Meta):
        fields = CustomUserSerializer.Meta.fields + (
            'recipes',
            'recipes_count'
        )

    def get_recipes(self, user):
        """Список рецептов пользователя."""
        recipes_limit = self.context.get('recipes_limit')
        recipes = user.author_recipes.all()
        if recipes_limit:
            recipes = recipes[:recipes_limit]
        return RecipeShortInfoSerializer(
            recipes,
            many=True,
            context=self.context
        ).data

    def get_recipes_count(self, user):
        """Возвращает количество рецептов."""
        return user.author_recipes.count()


class SubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор создания подписки."""
    class Meta:
        model = Subscriber
        fields = '__all__'
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Subscriber.objects.all(),
                fields=['user', 'author'],
                message=_('The user is already following the author')
            )
        ]

    def to_representation(self, instance):
        author = get_object_or_404(User, pk=instance.author.pk)
        return SubscribeInfoSerializer(
            instance=author,
            context=self.context
        ).data

    def validate(self, data):
        """Дополнительная проверка наличия подписки на себя."""
        if data['user'] == data['author']:
            raise serializers.ValidationError(_('User cannot follow himself.'))
        return data


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор избранного."""
    class Meta:
        model = Recipe.favorites.through
        fields = '__all__'
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Recipe.favorites.through.objects.all(),
                fields=['customuser', 'recipe'],
                message=_('Recipe already added to favorites')
            )
        ]

    def to_representation(self, instance):
        recipe = get_object_or_404(Recipe, pk=instance.recipe.pk)
        return RecipeShortInfoSerializer(
            instance=recipe,
            context=self.context
        ).data


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор списка покупок."""
    class Meta:
        model = Recipe.shopping_carts.through
        fields = '__all__'
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Recipe.shopping_carts.through.objects.all(),
                fields=['customuser', 'recipe'],
                message=_('Recipe already added to shopping list')
            )
        ]

    def to_representation(self, instance):
        recipe = get_object_or_404(Recipe, pk=instance.recipe.pk)
        return RecipeShortInfoSerializer(
            instance=recipe,
            context=self.context
        ).data


class RecipesParamsSerializer(serializers.Serializer):
    """Сериализатор query параметров для рецептов пользователей."""
    is_favorited = serializers.ChoiceField(
        required=False, choices=[0, 1]
    )
    is_in_shopping_cart = serializers.ChoiceField(
        required=False, choices=[0, 1]
    )
    author = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=CustomUser.objects.all()
    )
    tags = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Tag.objects.all(),
        slug_field='slug'
    )


class RecipesIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингридиента рецепта."""
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient'
    )
    name = serializers.ReadOnlyField(
        source='ingredient.name'
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class RecipesReadSerializer(RecipeShortInfoSerializer):
    """Сериализатор чтения данных рецепта."""
    tags = TagSerializer(many=True)
    author = CustomUserSerializer()
    ingredients = RecipesIngredientSerializer(
        many=True,
        source='recipe_ingredients'
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = RecipeShortInfoSerializer.Meta.fields + (
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'text',
        )

    def get_is_favorited(self, recipe):
        """Проверка наличия подписок у пользователя."""
        user = self.context.get('request').user
        return recipe.is_favorited(user)

    def get_is_in_shopping_cart(self, recipe):
        """Проверка наличия подписок у пользователя."""
        user = self.context.get('request').user
        return recipe.is_in_shopping_cart(user)


class RecipesWriteSerializer(serializers.ModelSerializer):
    """Сериализатор записи данных рецепта."""
    ingredients = RecipesIngredientSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    image = Base64ImageField(represent_in_base64=True)

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'author',
            'image',
            'name',
            'text',
            'cooking_time'
        )

    def _check_unique_id(self, values, error_message):
        """Проверка уникальности первичных ключей в списке записей values."""
        values_id = {value.pk for value in values}
        if len(values_id) != len(values):
            raise serializers.ValidationError(error_message)
        return True

    def validate_ingredients(self, ingredients):
        """Валидация уникальности идентификаторов ингредиентов."""
        self._check_unique_id(
            [ingredient['ingredient'] for ingredient in ingredients],
            _('ID ingredients not unique')
        )
        return ingredients

    def validate_tags(self, tags):
        """Валидация уникальности тегов."""
        self._check_unique_id(
            tags,
            _('ID tags not unique')
        )
        return tags

    def _get_ingredients_recipe(self, recipe, validated_ingredients):
        """Формирует список ингредиентов для записи в БД."""
        return [
            RecipeIngredient(
                recipe=recipe, **ingredient
            )
            for ingredient in validated_ingredients
        ]

    def _get_tags_recipe(self, recipe, validated_tags):
        """Формирует список тегов для записи в БД."""
        return [
            Recipe.tags.through(
                recipe=recipe, tag=tag
            )
            for tag in validated_tags
        ]

    def _set_ingredients_recipe(self, recipe, validated_ingredients):
        """Устанавливает список ингридиентов для рецепта в БД."""
        ingredients = self._get_ingredients_recipe(
            recipe, validated_ingredients
        )
        if ingredients:
            recipe.ingredients.clear()
            RecipeIngredient.objects.bulk_create(ingredients)

    def _set_tags_recipe(self, recipe, validated_tags):
        """Устанавливает список тегов для рецепта в БД."""
        tags = self._get_tags_recipe(recipe, validated_tags)
        if tags:
            recipe.tags.clear()
            Recipe.tags.through.objects.bulk_create(tags)

    def perform_recipe_action(self, validated_data, instance=None):
        """
        Выполнение в одной транзакции операций
        записи/обновления по рецепту, ингредиентам и тегам.
        """
        with transaction.atomic():
            ingredients = validated_data.pop('ingredients')
            tags = validated_data.pop('tags')
            if instance:
                for attr, value in validated_data.items():
                    setattr(instance, attr, value)
                instance.save()
            else:
                instance = Recipe.objects.create(**validated_data)
            self._set_ingredients_recipe(instance, ingredients)
            self._set_tags_recipe(instance, tags)
        return instance

    def create(self, validated_data):
        """Создает запись в БД по рецепту."""
        try:
            return self.perform_recipe_action(validated_data)
        except (IntegrityError, DatabaseError):
            self.fail(_('Cannot create recipe'))

    def update(self, instance, validated_data):
        """Обновление записи в БД по рецепту."""
        try:
            return self.perform_recipe_action(validated_data, instance)
        except (IntegrityError, DatabaseError):
            self.fail(_('Cannot update recipe'))

    def to_representation(self, instance):
        """Возвращает информацию по рецепту."""
        return RecipesReadSerializer(
            instance=instance,
            context=self.context
        ).data
