from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.utils import get_object_or_400


class UserDataViewSet(viewsets.GenericViewSet):
    """Базовый viewSet-класс  пользователь."""
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    user_field = None
    obj_field = None
    obj_model = None

    def get_serializer(self, *args, **kwargs):
        """Возвращает сериализатор с информацией в request data."""
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        if self.action != 'list':
            kwargs['data'] = self._get_request_data()
        return serializer_class(*args, **kwargs)

    def _get_pk_values(self):
        """Возвращает значения первичного составного ключа из запроса."""
        obj_id = self.kwargs.get('id')
        user_id = self.request.user.pk
        return user_id, obj_id

    def _get_pk_field(self):
        """Возвращает наименование полей составного ключа."""
        return (self.user_field, self.obj_field,)

    def _get_request_data(self):
        """Возвращает request data для запроса."""
        pk_values = self._get_pk_values()
        get_object_or_404(self.obj_model, pk=pk_values[1])
        return dict(zip(self._get_pk_field(), pk_values))

    def get_object(self):
        """Возвращает объект по первичному ключу."""
        obj_info = self._get_request_data()
        queryset = self.get_queryset()
        return get_object_or_400(queryset, **obj_info)
