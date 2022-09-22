from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """Пагинатор проекта."""
    page_size = 6
    page_size_query_param = 'limit'
