from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from api.settings import USER_ME
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CustomUser


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор модели категорий."""
    class Meta:
        exclude = ('id', 'description')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор модели жанров."""
    class Meta:
        exclude = ('id',)
        model = Genre


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        exclude = ('review',)
        model = Comment


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователей."""
    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate_username(self, value):
        if value.upper() == USER_ME:
            raise serializers.ValidationError('Недопустимое имя')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели отзывов."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    def validate(self, data):
        """Валидация - на одно произведение один отзыв."""
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (request.method == 'POST'
            and Review.objects.filter(
                title=title, author=author).exists()):
            raise ValidationError(
                'На одно произведение пользователь может '
                'оставить только один отзыв!'
            )
        return data

    class Meta:
        exclude = ('title',)
        model = Review


class TitlePostSerializer(serializers.ModelSerializer):
    """Сериализатор модели произведений - изменение."""
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        slug_field='slug',
    )

    class Meta:
        fields = '__all__'
        model = Title


class TitleGetSerializer(serializers.ModelSerializer):
    """Сериализатор модели произведений - чтение."""
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title
