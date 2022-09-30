from django.contrib.auth import get_user_model
from django.db import DatabaseError, IntegrityError, transaction
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from core.utils import (create_ordered_dicts_from_objects,
                        get_field_values_from_dict,
                        get_from_dicts_field_values,
                        get_from_objects_field_values)
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
        unique_values_id = set(values)
        if len(unique_values_id) != len(values):
            raise serializers.ValidationError(error_message)
        return True

    def validate_ingredients(self, ingredients):
        """Валидация уникальности ингредиентов."""
        ingredients_id = get_from_dicts_field_values(
            ingredients,
            'ingredient'
        )
        self._check_unique_id(
            ingredients_id,
            _('ID ingredients not unique')
        )
        return ingredients

    def validate_tags(self, tags):
        """Валидация уникальности тегов."""
        tags_id = get_from_objects_field_values(
            tags,
            'id'
        )
        self._check_unique_id(
            tags_id,
            _('ID tags not unique')
        )
        return tags

    def _get_ingredients_recipe(self, recipe, validated_ingredients):
        """Формирует список ингредиентов для записи в БД."""
        return [
            Recipe.ingredients.through(
                recipe=recipe, **ingredient
            )
            for ingredient in validated_ingredients
        ]

    def _get_tags_recipe(self, recipe, validated_tags):
        """Формирует список тегов для записи в БД."""
        return [
            Recipe.tags.through(
                recipe=recipe, **tag
            )
            for tag in validated_tags
        ]

    def _create_recipe_m2m_data(
        self, recipe, queryset, data, obj_generator
    ):
        """Создание связанных с рецептом данных."""
        bulk_objs = obj_generator(recipe, data)
        queryset.objects.bulk_create(bulk_objs)

    def _update_recipe_m2m_data(
        self, recipe, queryset, data, obj_generator, *fields
    ):
        """Обновление связанных с рецептом данных."""
        if not fields:
            raise ValueError(
                _('Recipe data cannot be set. Field list missing.')
            )
        new_data_id = set(get_from_dicts_field_values(data, *fields))
        db_values_id = set(
            queryset.objects.filter(
                recipe=recipe
            ).values_list(*fields)
        )
        update_id = set()
        if len(fields) > 1:
            update_id = new_data_id - db_values_id
            new_data_id = {(pk[0],) for pk in new_data_id}
            db_values_id = {(pk[0],) for pk in db_values_id}
        insert_id = new_data_id - db_values_id
        delete_id = db_values_id - new_data_id
        update_id = {id for id in update_id if (id[0],) not in insert_id}
        if delete_id:
            filter_id = {}
            filter_id['recipe'] = recipe
            filter_id[f'{fields[0]}__in'] = delete_id
            queryset.objects.filter(**filter_id).delete()
        if update_id:
            filter_id = {}
            update_fields = fields[1:]
            filter_id['recipe'] = recipe
            for data_id in update_id:
                filter_id[f'{fields[0]}'] = data_id[0]
                update_values = dict(zip(update_fields, data_id[1:]))
                queryset.objects.filter(**filter_id).update(**update_values)
        if insert_id:
            insert_data = [
                obj for obj in data if get_field_values_from_dict(
                    obj, fields[0]
                ) in insert_id
            ]
            self._create_recipe_m2m_data(
                recipe, queryset, insert_data, obj_generator
            )

    def create(self, validated_data):
        """Создает запись в БД по рецепту."""
        try:
            return self.perform_recipe_create(validated_data)
        except (IntegrityError, DatabaseError):
            self.fail(_('Cannot create recipe'))

    def perform_recipe_create(self, validated_data):
        """
        Выполнение в одной транзакции операций
        записи данных по рецепту, ингредиентам и тегам.
        """
        with transaction.atomic():
            ingredients = validated_data.pop('ingredients')
            tags = validated_data.pop('tags')
            tags = create_ordered_dicts_from_objects(tags, 'tag')
            instance = Recipe.objects.create(**validated_data)
            self._create_recipe_m2m_data(
                instance,
                Recipe.ingredients.through,
                ingredients,
                self._get_ingredients_recipe
            )
            self._create_recipe_m2m_data(
                instance,
                Recipe.tags.through,
                tags,
                self._get_tags_recipe
            )
        return instance

    def update(self, instance, validated_data):
        """Обновление записи в БД по рецепту."""
        try:
            return self.perform_recipe_update(validated_data, instance)
        except (IntegrityError, DatabaseError):
            self.fail(_('Cannot update recipe'))

    def perform_recipe_update(self, validated_data, instance):
        """
        Выполнение в одной транзакции операций
        по обновлению данных по рецепту, ингредиентам и тегам.
        """
        with transaction.atomic():
            ingredients = validated_data.pop('ingredients')
            tags = validated_data.pop('tags')
            tags = create_ordered_dicts_from_objects(tags, 'tag')
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            self._update_recipe_m2m_data(
                instance,
                Recipe.ingredients.through,
                ingredients,
                self._get_ingredients_recipe,
                'ingredient',
                'amount'
            )
            self._update_recipe_m2m_data(
                instance,
                Recipe.tags.through,
                tags,
                self._get_tags_recipe,
                'tag'
            )
        return instance

    def to_representation(self, instance):
        """Возвращает информацию по рецепту."""
        return RecipesReadSerializer(
            instance=instance,
            context=self.context
        ).data
