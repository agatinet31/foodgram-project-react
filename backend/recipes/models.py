from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, validate_slug
from django.db import models
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
    color = models.CharField(
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
        unique=True,
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
        max_length=10,
        validators=[validate_only_letters],
        help_text=_('Required. Enter measurement_unit, please.'),
    )

    class Meta:
        """Метаданные модели ингридиентов."""
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient_name_and_unit'
            )
        ]
        ordering = ['name']
        verbose_name = _('ingredient')
        verbose_name_plural = _('ingredients')

    def __str__(self):
        """Метод возвращает имя ингридиента."""
        return self.name


class Recipe(models.Model):
    """Модель рецепта."""
    name = models.CharField(
        _('name'),
        max_length=500,
        unique=True,
        validators=[validate_simple_name],
        help_text=_(
            'Required. Enter name recipe, please.'),
        error_messages={
            'unique': _('A recipe with that name already exists.'),
        }
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipes',
        blank=True,
        verbose_name=_('ingredients'),
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        blank=True,
        verbose_name=_('tags'),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name=_('author'),
        help_text=_('Required. Enter author, please. ')
    )
    favorites = models.ManyToManyField(
        User,
        related_name='recipes',
        blank=True,
        verbose_name=_('favorites'),
    )
    pub_date = models.DateTimeField(
        _('public date'),
        auto_now_add=True,
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
        _('cooking_time'),
        validators=[
            MinValueValidator(
                1, message=_('Cooking time must be more than 1 minute')
            )
        ]
    )

    class Meta:
        """Метаданные модели рецептов."""
        indexes = [
            models.Index(fields=['text'], name='recipe_text_idx'),
            models.Index(fields=['pub_date'], name='recipe_pub_date_idx'),
        ]
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient_name_and_unit'
            )
        ]
        verbose_name = _('recipe')
        verbose_name_plural = _('recipes')

    def __str__(self):
        """Метод возвращает название рецепта."""
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, models.CASCADE, to_field="rname")
    ingredient = models.ForeignKey(Ingredient, models.CASCADE, to_field="iname")
    amount = models.PositiveSmallIntegerField(
        _('amount'),
        validators=[
            MinValueValidator(
                1, message=_('Ingredient quantity must be greater than 0')
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

    def get_ingredient_recipe(self):
        """Метод возвращает информацию по ингридиенту рецепта."""
        return (
            self.recipe.pk, self.ingredient.pk, self.amount
        )

    def __str__(self):
        """Метод возвращает информацию по ингридиенту рецепта."""
        return (
            f'{self.recipe.name}:{self.ingredient.name}, '
            f'{self.amount} {self.ingredient.measurement_unit}'
        )
