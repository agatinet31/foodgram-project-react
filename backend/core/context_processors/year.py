from django.utils import timezone


def year(request):
    """Добавляет в контекст переменную year с значением текущего года."""
    year = timezone.now().year
    return {
        'year': year
    }
