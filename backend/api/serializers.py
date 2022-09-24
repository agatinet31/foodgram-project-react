from django.contrib.auth import get_user_model
# from django.utils.translation import gettext_lazy as _
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


class SubscribeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания подписки."""
    class Meta:
        model = Subscriber
        fields = '__all__'

    def create(self, validated_data):
        return Subscriber.objects.create(**validated_data)

    def validate(self, attrs):
        instance = Subscriber(**attrs)
        instance.full_clean()
        return attrs


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
