from collections import OrderedDict

from django.shortcuts import _get_queryset
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ParseError, PermissionDenied


def get_field_values_from_object(obj, *fields):
    """
    Возвращает кортеж из значений атрибутов fields объекта.
    """
    if not isinstance(obj, object):
        raise TypeError(_('Unable to get field data'))
    return (
        getattr(obj, field) for field in fields if hasattr(obj, field)
    )


def get_from_objects_field_values(records, *fields):
    """
    Возвращает список, состоящий из кортежей значений полей fields
    списка объектов records.
    """
    return [
        get_field_values_from_object(obj, *fields) for obj in records
    ]


def get_field_values_from_dict(data, *fields):
    """
    Возвращает кортеж значений полей из словаря data.
    """
    try:
        field_values = []
        for key in fields:
            value = data[key]
            if isinstance(value, object) and hasattr(value, 'id'):
                value = int(value.id)
            field_values.append(value)
        return tuple(field_values)
    except (TypeError, KeyError, ValueError):
        return None


def get_from_dicts_field_values(records, *fields):
    """
    Возвращает список, состоящий из кортежей значений полей fields
    из списка словарей records.
    """
    return [
        get_field_values_from_dict(data, *fields) for data in records
    ]


def create_ordered_dicts_from_objects(objs, key):
    """Создает список словарей на основании списка объектов."""
    return [
        OrderedDict({key: obj}) for obj in objs
    ]


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
