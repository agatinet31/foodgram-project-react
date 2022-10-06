from itertools import chain

from rest_framework import filters


class IngredientFilter(filters.BaseFilterBackend):
    """Фильтр ингредиентов по наименованию."""
    def filter_queryset(self, request, queryset, view):
        name_query_params = 'name'
        value = request.query_params.get(name_query_params, None)
        if value:
            queryset_istartswith = queryset.filter(
                name__istartswith=value
            )
            queryset_contains = queryset.filter(
                name__contains=value
            ).difference(queryset_istartswith).order_by(name_query_params)
            return list(chain(queryset_istartswith, queryset_contains))
        return queryset
