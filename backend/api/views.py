from django.contrib.auth import get_user_model
from django.db.models import Sum
# from django.shortcuts import get_object_or_404
# from django.utils.translation import gettext_lazy as _
from djoser.views import UserViewSet
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.decorators import action
# , status
# viewsets
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.pagination import CustomPagination
from api.report import PDFPrint
from api.serializers import (FavoriteSerializer, IngredientSerializer,
                             RecipesParamsSerializer, RecipesReadSerializer,
                             RecipesWriteSerializer, ShoppingCartSerializer,
                             SubscribeParamsSerializer, SubscribeSerializer,
                             TagSerializer)
from api.viewsets import UserDataViewSet
# from core.utils import get_object_or_400
from recipes.models import Ingredient, Recipe, Tag
from users.models import Subscriber

# from api.filters import TitlesFilter
# from api.permissions import AnyReadOnly, IsAdmin

User = get_user_model()


class UserListViewSet(UserViewSet):
    """ViewSet-класс пользователей для эндпоинта users."""
    pagination_class = CustomPagination


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


class SubscribeViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       UserDataViewSet):
    """ViewSet-класс для модели подписок пользователей."""
    serializer_class = SubscribeSerializer
    pagination_class = CustomPagination
    user_field = 'user'
    obj_field = 'author'
    obj_model = User

    def get_serializer_context(self):
        """Возвращает контекст сериализатора."""
        context = super().get_serializer_context()
        query = SubscribeParamsSerializer(data=self.request.query_params)
        if query.is_valid(raise_exception=True):
            query_params = query.validated_data
            context['recipes_limit'] = query_params.get('recipes_limit')
        return context

    def get_queryset(self):
        """Возвращает выборку данных по подпискам для текущего пользователя."""
        return Subscriber.objects.filter(user=self.request.user)


class FavoriteViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      UserDataViewSet):
    """ViewSet-класс для избранного."""
    serializer_class = FavoriteSerializer
    user_field = 'customuser'
    obj_field = 'recipe'
    obj_model = Recipe

    def get_queryset(self):
        """Возвращает выборку данных по избраному для текущего пользователя."""
        return Recipe.favorites.through.objects.filter(
            customuser_id=self.request.user.pk
        )


class ShoppingCartViewSet(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          UserDataViewSet):
    """ViewSet-класс для избранного."""
    serializer_class = ShoppingCartSerializer
    user_field = 'customuser'
    obj_field = 'recipe'
    obj_model = Recipe

    def get_queryset(self):
        """
        Возвращает выборку данных по списку покупок
        для текущего пользователя.
        """
        return Recipe.shopping_carts.through.objects.filter(
            customuser_id=self.request.user.pk
        )

    @action(methods=['get'], detail=False)
    def download_shopping_cart(self, request):
        """Формирует файл списка покупок."""
        user = self.request.user
        shopping_carts_ingredients = user.shopping_cart_recipes.values(
            'ingredients__name', 'ingredients__measurement_unit'
        ).annotate(
            total=Sum('recipe_ingredients__amount')
        ).order_by('ingredients__name')
        return PDFPrint().create_pdf(shopping_carts_ingredients)


class RecipesViewSet(viewsets.ModelViewSet):
    """ViewSet-класс для модели рецептов."""
    queryset = Recipe.objects.all()
    pagination_class = CustomPagination
    lookup_field = 'id'

    def get_serializer_context(self):
        """Возвращает контекст сериализатора."""
        context = super().get_serializer_context()
        query = RecipesParamsSerializer(data=self.request.query_params)
        if query.is_valid(raise_exception=True):
            query_params = query.validated_data
            context['is_favorited'] = query_params.get(
                'is_favorited'
            )
            context['is_in_shopping_cart'] = query_params.get(
                'is_in_shopping_cart'
            )
            author = query_params.get('author')
            context['author'] = author.pk if author else None
            tags_slug = query_params.get('tags')
            context['tags'] = (
                [slug.pk for slug in tags_slug] if tags_slug else None
            )
        return context

    def get_queryset(self):
        """Возвращает выборку данных по рецептам."""
        queryset = super().get_queryset()
        context = self.get_serializer_context()
        user = self.request.user
        if context['is_favorited']:
            queryset = queryset.filter(favorites__id=user.pk)
        if context['is_in_shopping_cart']:
            queryset = queryset.filter(shopping_carts__id=user.pk)
        if context['author']:
            queryset = queryset.filter(author__id=context['author'])
        if context['tags']:
            queryset = queryset.filter(tags__id__in=context['tags']).distinct()
        return queryset.all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipesReadSerializer
        return RecipesWriteSerializer
