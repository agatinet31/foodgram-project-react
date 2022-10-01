from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly


class IsAuthorOrAuthenticatedOrReadOnly(IsAuthenticatedOrReadOnly):
    """
    Класс предоставляющий следующие права доступа:
        - редактирования и удаления только для автора объекта
          по полю author
        - добавление только аутентифицированным пользователям
        - остальным пользователям только чтение.
    """
    def has_object_permission(self, request, view, obj):
        """Проверка авторства объекта по полю author."""
        return request.method in SAFE_METHODS or obj.author == request.user
