from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from djoser.serializers import UserSerializer
# from django.db import IntegrityError, transaction
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from users.models import Subscriber

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
        """Возвращает абсолюьный URL картинки."""
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


class SlugListField(serializers.ListField):
    """Класс поля сериализатора для списка слагов."""
    child = serializers.SlugField()


class IntegerListField(serializers.ListField):
    """Класс поля сериализатора для списка слагов."""
    child = serializers.IntegerField(min_value=1)


class RecipesParamsSerializer(serializers.Serializer):
    """Сериализатор query параметров для рецептов пользователей."""
    is_favorited = serializers.ChoiceField(
        required=False, choices=[0, 1]
    )
    is_in_shopping_cart = serializers.ChoiceField(
        required=False, choices=[0, 1]
    )
    author = serializers.IntegerField(
        required=False, min_value=1,
    )
    tags = SlugListField(required=False, allow_empty=True)


class RecipesIngridientSerializer(serializers.ModelSerializer):
    """Сериализатор ингридиента рецепта."""
    id = serializers.IntegerField(source='ingredient')
    # recipe

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'amount',
        )


class RecipesWriteSerializer(serializers.ModelSerializer):
    """Сериализатор записи данных рецепта."""
    ingredients = RecipesIngridientSerializer(many=True)
    tags = IntegerListField()
    image = Base64ImageField(represent_in_base64=True)
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'author',
            'name',
            'text',
            'cooking_time'
        )


class RecipesReadSerializer(RecipeShortInfoSerializer):
    """Сериализатор чтения данных рецепта."""
    tags = TagSerializer(many=True)
    author = CustomUserSerializer()
    ingredients = IngredientSerializer(many=True)

    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = RecipeShortInfoSerializer.Meta.fields + (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )

    def get_is_favorited(self, recipe):
        """Проверка наличия подписок у пользователя."""
        user = self.context.get('request').user
        return recipe.is_favorited(user)

    def get_is_in_shopping_cart(self, recipe):
        """Проверка наличия подписок у пользователя."""
        user = self.context.get('request').user
        return recipe.is_in_shopping_cart(user)
