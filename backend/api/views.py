from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
# from django.shortcuts import get_object_or_404
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters  # , mixins
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.serializers import TagSerializer, IngredientSerializer
from recipes.models import Tag, Ingredient

# from api.filters import TitlesFilter
# from api.permissions import AnyReadOnly, IsAdmin

User = get_user_model()


"""
class CreateUserViewSet(UserViewSet):
    ViewSet-класс регистрации нового пользователя.
    queryset = User.objects.all()
    serializer_class = CustomUserCreateSerializer
    # http_method_names = ["post", "get", "put", "delete"]
"""


class TagViewSet(ReadOnlyModelViewSet):
    """ViewSet-класс для просмотра информации по тегам."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    """ViewSet-класс для просмотра информации по ингридиентам."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)
