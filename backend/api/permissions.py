from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from .settings import USER_ME


class DeafaultYamdbPermission(IsAuthenticatedOrReadOnly):
    """
    Класс предоставляющий следующие права доступа:
        - редактирования и удаления только для автора объекта
          по полю author, модератору и администратору
        - добавление только аутентифицированным пользователям
        - остальным пользователям только чтение.
    """
    def has_object_permission(self, request, view, obj):
        """
        Проверка авторства объекта по полю author,
        а также прав доступа на основании роли пользователя.
        """
        return (
            request.method in SAFE_METHODS
            or request.user.is_superuser
            or request.user.is_authenticated
            and (
                obj.author == request.user
                or request.user.is_powereduser
            )
        )


class AnyReadOnly(BasePermission):
    """
    Класс предоставляющий всем права доступа только на чтение.
    """
    def has_permission(self, request, view):
        """Доступ только на чтение."""
        return request.method in SAFE_METHODS


class IsAdmin(IsAuthenticated):
    """
    Класс предоставляющий права доступа только администратору.
    """
    def has_permission(self, request, view):
        """Проверка доступа для администратора."""
        return (
            super().has_permission(request, view) and request.user.is_admin
            or request.user.is_superuser
        )


class UserAccountPermission(IsAdmin):
    """
    Класс предоставляющий права доступа пользователю me.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        user_name = view.kwargs.get('username')
        if user_name is None or user_name.upper() != USER_ME:
            return super().has_permission(request, view)
        if request.method == 'DELETE':
            raise MethodNotAllowed('Нельзя удалить себя')
        return request.method in ('GET', 'PATCH')
