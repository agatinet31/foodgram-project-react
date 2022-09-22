from django.contrib.auth import get_user_model
from django.shortcuts import get_list_or_404, get_object_or_404
from djoser.views import UserViewSet
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
# from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.pagination import CustomPagination
from api.serializers import (IngredientSerializer, SubscribeSerializer,
                             TagSerializer)
from recipes.models import Ingredient, Tag
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
                       viewsets.GenericViewSet):
    """ViewSet-класс для моделей подписок."""
    serializer_class = SubscribeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return get_list_or_404(
            User, author_subscribers__user=self.request.user
        )

    def _get_user_and_author(self, request, *args, **kwargs):
        """Запрос информаци по пользователю и автору."""
        author_id = self.kwargs.get('id')
        if author_id is None:
            return Response(status.HTTP_400_BAD_REQUEST)
        author = get_object_or_404(User, pk=author_id)
        user = request.user
        return dict(user=user, author=author)

    def create(self, request, *args, **kwargs):
        """Подписаться на пользователя."""
        data = self._get_user_and_author(request, *args, **kwargs)
        Subscriber.objects.create(**data)
        return Response(status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """Отписаться от пользователя."""
        data = self._get_user_and_author(request, *args, **kwargs)
        subscribe = get_object_or_404(Subscriber, **data)
        subscribe.delete()
        return Response(status.HTTP_204_NO_CONTENT)
