from django.core.exceptions import ValidationError
from django.utils import timezone


def validation_year(year):
    """Валидация поля год."""
    if year > timezone.now().year:
        raise ValidationError(
            ('Значение года %(year)s не может быть больше текущего!'),
            params={'year': year},
        )
