from rest_framework.permissions import IsAuthenticated


class IsOwnerOnly(IsAuthenticated):
    """
    Класс предоставляющий права доступа только владельцу.
    """
    def has_object_permission(self, request, view, obj):
        """
        Проверка авторства объекта.
        """
        return (hasattr(obj, 'author') and obj.author == request.user
                or hasattr(obj, 'user') and obj.user == request.user)
