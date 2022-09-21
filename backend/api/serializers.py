from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers

from recipes.models import Tag, Ingredient
# from rest_framework.exceptions import ValidationError
# from rest_framework.generics import get_object_or_404

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """Сериализатор данных пользователя."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_is_subscribed(self, obj):
        """Проверка наличия подписок у пользователя."""
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return request.user.is_subscribed


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
