from rest_framework import filters, mixins, viewsets
from rest_framework.viewsets import ModelViewSet

from .permissions import AnyReadOnly, DeafaultYamdbPermission, IsAdmin


class YamdbBaseViewSet(ModelViewSet):
    """Базовый ViewSet."""
    permission_classes = [DeafaultYamdbPermission]


class AuthViewSet(mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    """
    Класс Viewset обеспечивающий выполнение `create()` функции.
    Доступ только у администратора.
    """
    permission_classes = [IsAdmin]


class AdminOrReadOnlyViewSet(mixins.CreateModelMixin,
                             mixins.ListModelMixin,
                             mixins.DestroyModelMixin,
                             viewsets.GenericViewSet):
    """
    Класс Viewset обеспечивающий выполнение
     `create()`, `destroy()` и `list()` функций для справочников системы.
    Доступ на изменение только у администратора, у остальных только чтение.
    """
    permission_classes = [AnyReadOnly | IsAdmin]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)
    lookup_field = 'slug'
