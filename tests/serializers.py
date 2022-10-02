from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    """Сериализатор данных пользователя."""
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()


class UserCreateRequestSerializer(UserSerializer):
    """Сериализатор данных нового пользователя."""
    password = serializers.CharField()


class UserCreateResponseSerializer(UserSerializer):
    """Сериализатор данных нового пользователя."""
    id = serializers.IntegerField()


class UserResponseSerializer(UserCreateResponseSerializer):
    """Сериализатор данных по запрашиваемому пользователю."""
    is_subscribed = serializers.BooleanField()


class UserListResponseSerializer(serializers.ListSerializer):
    """Сериализатор списка данных пользователей."""
    child = UserResponseSerializer()


class UserRequestNewPasswordSerializer(serializers.Serializer):
    """Сериализатор запроса нового пароля пользователя."""
    new_password = serializers.CharField()
    current_password = serializers.CharField()


class UserRequestLoginSerializer(serializers.Serializer):
    """Сериализатор запроса токена пользователя."""
    email = serializers.CharField()
    password = serializers.CharField()


class UserResponseLoginSerializer(serializers.Serializer):
    """Сериализатор токена пользователя."""
    auth_token = serializers.CharField()


class TagSerializer(serializers.Serializer):
    """Сериализатор тегов."""
    id = serializers.IntegerField()
    name = serializers.CharField()
    color = serializers.CharField()
    slug = serializers.SlugField()


class TagListField(serializers.ListField):
    """Список тегов."""
    child = TagSerializer()


class IngredientSerializer(serializers.Serializer):
    """Сериализатор ингридиентов."""
    id = serializers.IntegerField()
    name = serializers.CharField()
    measurement_unit = serializers.CharField()


class IngredientListField(serializers.ListField):
    """Список ингредиентов."""
    child = IngredientSerializer()


class RecipeShortInfoSerializer(serializers.Serializer):
    """Сериализатор с краткой информацией рецепта."""
    id = serializers.IntegerField()
    name = serializers.CharField()
    image = serializers.CharField()
    cooking_time = serializers.IntegerField()


class SubscribeInfoSerializer(UserResponseSerializer):
    """Сериализатор информации по подпискам пользователей."""
    recipes = RecipeShortInfoSerializer(many=True)
    recipes_count = serializers.IntegerField()


class SubscribeInfoListField(serializers.ListField):
    child = SubscribeInfoSerializer()


class RecipesIngredientSerializer(IngredientSerializer):
    """Сериализатор ингридиента рецепта."""
    amount = serializers.IntegerField()


class RecipesResponseSerializer(RecipeShortInfoSerializer):
    """Сериализатор чтения данных рецепта."""
    tags = TagSerializer(many=True)
    author = UserResponseSerializer()
    ingredients = RecipesIngredientSerializer(many=True)
    is_favorited = serializers.BooleanField()
    is_in_shopping_cart = serializers.BooleanField()


class RecipesResponseListField(serializers.ListField):
    child = RecipesResponseSerializer()


class RecipesIngredientShortSerializer(serializers.Serializer):
    """Сериализатор краткой информации по ингридиенту рецепта."""
    id = serializers.IntegerField()
    amount = serializers.IntegerField()


class IntegerListField(serializers.ListField):
    child = serializers.IntegerField()


class RecipesRequestSerializer(serializers.Serializer):
    """Сериализатор запроса данных по рецепту."""
    ingredients = RecipesIngredientShortSerializer(many=True)
    tags = IntegerListField()
    image = serializers.CharField()
    name = serializers.CharField()
    text = serializers.CharField()
    cooking_time = serializers.IntegerField()
