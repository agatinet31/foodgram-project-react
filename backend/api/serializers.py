from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
# from django.db import IntegrityError, transaction
from django.utils.translation import gettext_lazy as _
from djoser.serializers import UserSerializer
from rest_framework import serializers

from recipes.models import Ingredient, Recipe, Tag
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
        if user.is_authenticated:
            return user.is_subscribed(author)
        return False


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
