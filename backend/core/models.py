from django.core.validators import validate_slug
from django.db import models
from django.utils.translation import gettext_lazy as _


class SlugDataModel(models.Model):
    """Абстрактная Slug модель."""
    name = models.CharField(
        _('name'),
        unique=True,
        max_length=256
    )
    slug = models.SlugField(
        _('slug'),
        unique=True,
        max_length=50,
        validators=[validate_slug]
    )

    class Meta:
        """Метаданые абстрактной модели."""
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name
