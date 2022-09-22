from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, validate_slug
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.validators import (validate_color_hex_code, validate_only_letters,
                             validate_simple_name, validate_tag)

User = get_user_model()


class Tag(models.Model):
    """Модель тега."""
    name = models.CharField(
        _('name'),
        max_length=150,
        unique=True,
        validators=[validate_tag],
        help_text=_(
            'Required. Enter tag name, please. '
            '150 characters or fewer. Letters, digit only'
            'and first symbol can be `#`'
        ),
        error_messages={
            'unique': _('A tag with that name already exists.'),
        }
    )
    color = ColorField(
        _('color HEX-code'),
        max_length=7,
        unique=True,
        validators=[validate_color_hex_code],
        help_text=_('Required. Enter HEX-code color, please.'),
        error_messages={
            'unique': _('A tag with that color already exists.'),
        }
    )
    slug = models.SlugField(
        _('slug'),
        unique=True,
        max_length=50,
        validators=[validate_slug],
        help_text=_('Required. Enter slug tag, please.'),
        error_messages={
            'unique': _('A tag with that slug already exists.'),
        }
    )

    class Meta:
        """Метаданные модели тегов."""
        ordering = ['name']
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        """Метод возвращает имя тега."""
        return self.name


class Ingredient(models.Model):
    """Модель ингридиента."""
    name = models.CharField(
        _('name'),
        max_length=250,
        validators=[validate_simple_name],
        help_text=_(
            'Required. Enter ingredient name, please. '
            '250 characters or fewer. '
            'Letters, digit symbols _ ( " ). '
            'The first symbol only letter.'
        ),
        error_messages={
            'unique': _('A ingredient with that name already exists.'),
        }
    )
    measurement_unit = models.CharField(
        _('measurement_unit'),
        max_length=50,
        validators=[validate_only_letters],
        help_text=_('Required. Enter measurement_unit, please.'),
    )

    class Meta:
        """Метаданные модели ингридиентов."""
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_name_measurement_unit'
            )
        ]
        ordering = ['name']
        verbose_name = _('ingredient')
        verbose_name_plural = _('ingredients')

    def __str__(self):
        """Метод возвращает имя ингридиента и единицу измерения."""
        return f'{self.name} ({self.measurement_unit})'


class Recipe(models.Model):
    """Модель рецепта."""
    name = models.CharField(
        _('name'),
        max_length=500,
        validators=[validate_simple_name],
        help_text=_(
            'Required. Enter name recipe, please.'),
    )
    pub_date = models.DateTimeField(
        _('public date'),
        default=timezone.now,
        db_index=True
    )
    image = models.ImageField(
        _('image'),
        upload_to='recipes/',
    )
    text = models.TextField(
        _('recipe text'),
    )
    cooking_time = models.PositiveSmallIntegerField(
        _('cooking time (minutes)'),
        validators=[
            MinValueValidator(
                1, message=_('Minimum cooking time 1 minute')
            )
        ]
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name=_('ingredients'),
        blank=True,
        through='RecipeIngredient',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name=_('tags'),
        blank=True,
        related_name='recipes',
    )
    author = models.ForeignKey(
        User,
        verbose_name=_('author'),
        on_delete=models.CASCADE,
        related_name='author_recipes',
        help_text=_('Required. Enter author, please. ')
    )
    favorites = models.ManyToManyField(
        User,
        verbose_name=_('favorites'),
        blank=True,
        related_name='favorite_recipes',
    )
    shopping_carts = models.ManyToManyField(
        User,
        verbose_name=_('shopping_carts'),
        blank=True,
        related_name='shopping_cart_recipes',
    )

    class Meta:
        """Метаданные модели рецептов."""
        indexes = [
            models.Index(fields=['name'], name='recipe_name_idx'),
            models.Index(fields=['text'], name='recipe_text_idx'),
            models.Index(fields=['pub_date'], name='recipe_pub_date_idx'),
        ]
        ordering = ['-pub_date']
        verbose_name = _('recipe')
        verbose_name_plural = _('recipes')

    @property
    def is_favorited(self):
        """Проверка наличия рецепта в избранном у пользователей."""
        return self.favorites.exists()

    @property
    def is_in_shopping_cart(self):
        """Проверка наличия рецепта в списке покупок у пользователей."""
        return self.shopping_carts.exists()

    def __str__(self):
        """Метод возвращает название рецепта."""
        return self.name


class RecipeIngredient(models.Model):
    """Модель ингридиентов рецепта."""
    recipe = models.ForeignKey(
        Recipe,
        verbose_name=_('recipe'),
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name=_('ingredient'),
        on_delete=models.CASCADE,
        related_name='ingredient_recipes'
    )
    amount = models.PositiveSmallIntegerField(
        _('amount'),
        validators=[
            MinValueValidator(
                1, message=_(
                    'The minimum quantity of an ingredient in a recipe is 1'
                )
            )
        ]
    )

    class Meta:
        """Метаданные модели ингридиентов рецепта."""
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            )
        ]
        verbose_name = _('recipe ingredient')
        verbose_name_plural = _('recipe ingredients')

    def __str__(self):
        """Метод возвращает информацию по ингридиенту рецепта."""
        return f'{self.ingredient} - {self.amount}'
