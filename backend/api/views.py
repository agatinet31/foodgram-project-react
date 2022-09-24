from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
# from django.utils.translation import gettext_lazy as _
from djoser.views import UserViewSet
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
# from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.pagination import CustomPagination
from api.serializers import (IngredientSerializer, SubscribeCreateSerializer,
                             SubscribeInfoSerializer,
                             SubscribeParamsSerializer, TagSerializer)
from core.utils import get_object_or_400
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
    serializer_class = SubscribeInfoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        query = SubscribeParamsSerializer(data=self.request.query_params)
        if query.is_valid(raise_exception=True):
            query_params = query.validated_data
            context['request'] = self.request
            context['recipes_limit'] = query_params.get('recipes_limit')
        return context

    def get_queryset(self):
        return User.objects.filter(author_subscribers__user=self.request.user)

    def _get_user_and_author_or_404(self, request):
        """Запрос информаци по пользователю и автору."""
        author_id = self.kwargs.get('id')
        get_object_or_404(User, pk=author_id)
        user_id = request.user.pk
        return dict(user=user_id, author=author_id)

    def create(self, request, *args, **kwargs):
        """Подписаться на автора рецепта."""
        data = self._get_user_and_author_or_404(request)
        serializer = SubscribeCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        author = get_object_or_404(User, pk=data['author'])
        return Response(
            SubscribeInfoSerializer(
                instance=author,
                context=self.get_serializer_context()
            ).data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, *args, **kwargs):
        """Отписаться от пользователя."""
        data = self._get_user_and_author_or_404(request)
        subscribe = get_object_or_400(Subscriber, **data)
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
