from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers

from core.utils import get_int
from recipes.models import Ingredient, Recipe, Tag

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
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class SubscribeSerializer(CustomUserSerializer):
    """Сериализатор подписок на пользователей."""
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(CustomUserSerializer.Meta):
        fields = CustomUserSerializer.Meta.fields + (
            'recipes',
            'recipes_count'
        )

    def get_recipes(self, user):
        """Список рецептов ."""
        request = self.context.get('request')
        recipes_limit = get_int(request.GET.get('recipes_limit'))
        """
        queryset = Recipe.objects.filter(author__id=obj.id).order_by('id')[
                :recipes_limit]
        """
        queryset = None
        return RecipeShortInfoSerializer(queryset, many=True).data

    def get_recipes_count(self, user):
        return 0
