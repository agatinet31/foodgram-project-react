from django.shortcuts import _get_queryset
from rest_framework.exceptions import ParseError, PermissionDenied


def get_int(str):
    """Безопасное преобразование строки в в целое число."""
    try:
        return int(str)
    except (TypeError, ValueError):
        return None


def get_pk_from_dict(data, key):
    """
    Возвращает значение первичного ключа pk
    из словаря data.
    """
    try:
        val = data[key]
        if isinstance(val, object) and hasattr(val, 'id'):
            return val.id
        return int(val)
    except (TypeError, KeyError, ValueError):
        return None


def get_object_or_400(klass, *args, **kwargs):
    """
    Возвращает один объект модели, в противном случае 400 ошибка.
    """
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist as e:
        raise ParseError(*e.args)
    except queryset.model.MultipleObjectsReturned as e:
        raise ParseError(*e.args)


def get_object_or_403(klass, *args, **kwargs):
    """
    Возвращает один объект модели, в противном случае 403 ошибка.
    """
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist as e:
        raise PermissionDenied(*e.args)
    except queryset.model.MultipleObjectsReturned as e:
        raise PermissionDenied(*e.args)


def is_exists_user_info(queryset, user):
    """
    Проверка наличия связаной информации по пользователю в queryset.
    """
    if user.is_anonymous:
        return False
    return queryset.filter(pk=user.pk).exists()
