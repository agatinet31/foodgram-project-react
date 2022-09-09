from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator, validate_slug
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Tag(models.Model):
    """Модель тега."""
    name = models.CharField(
        _('name'),
        max_length=250,
        unique=True,
        validators=[],
        help_text=_(
            'Required. Enter tag name, please. '
            '250 characters or fewer. Letters only.'
        ),
    )
    color = models.CharField(
        _('color'),
        max_length=10,
        unique=True,
        validators=[],
        help_text=_('Required. Enter color, please.'),
    )
    slug = models.SlugField(
        _('slug'),
        unique=True,
        max_length=50,
        validators=[validate_slug]
    )


class Ingredient(models.Model):
    """Модель ингридиента."""
    name = models.CharField(
        _('name'),
        max_length=250,
        unique=True,
        validators=[],
        help_text=_(
            'Required. Enter ingredient name, please. '
            '250 characters or fewer. Letters only.'
        ),
    )
    measurement_unit = models.CharField(
        _('measurement_unit'),
        max_length=10,
        validators=[],
        help_text=_('Required. Enter measurement_unit, please.'),
    )


class Recipe(models.Model):
    """Модель рецепта."""
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        blank=True,
        symmetrical=False
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name=_('author'),
        help_text=_('Required. Enter author, please. ')
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        blank=True,
        symmetrical=False
    )
    name = models.CharField(
        _('name'),
        max_length=500,
        unique=True,
        validators=[],
        help_text=_(
            'Required. Enter name recipe, please.'),
    )
    image = models.ImageField(
        'Изображение',
        upload_to='recipes/',
    )
    text = models.TextField(
        'Описание рецепта'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=(
            MinValueValidator(
                1, message='Время должно быть больше 1 минуты'),),
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
