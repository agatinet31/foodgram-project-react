from django_filters import rest_framework as filters

from reviews.models import Title


class TitlesFilter(filters.FilterSet):
    """Фильтр произведений."""
    genre = filters.CharFilter(
        field_name='genre__slug',
        lookup_expr='icontains'
    )
    category = filters.CharFilter(
        field_name='category__slug',
        lookup_expr='icontains'
    )
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )

    class Meta:
        fields = ('name', 'year', 'genre', 'category',)
        model = Title
