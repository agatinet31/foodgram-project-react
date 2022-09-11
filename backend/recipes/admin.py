from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Конфигурация для модели Tag в админке."""
    list_display = ('name', 'color', 'slug',)
    list_filter = ('name', 'slug',)
    search_fields = ('name',)
    empty_value_display = _('empty')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Конфигурация для модели Ingredient в админке."""
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = _('empty')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Конфигурация для модели Recipe в админке."""
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'author',
                'pub_date',
                'tags',
                'favorites',
                'amount_favorites',
                'shopping_carts',
                'image',
                'text',
                'cooking_time',
            )
        }),
    )
    list_display = ('name', 'author',)
    list_filter = ('author', 'name', 'tags')
    search_fields = ('name',)
    filter_horizontal = ('tags', 'favorites', 'shopping_carts',)
    empty_value_display = _('empty')

    def has_add_permission(self, request):
        """Запрет добавления рецепта в админке."""
        return False

    @staticmethod
    def amount_favorites(recipe):
        return recipe.favorites.count()


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    """Конфигурация для модели RecipeIngredient в админке."""
    list_display = ('recipe', 'ingredient', 'amount')
    list_filter = ('recipe', 'ingredient',)
    search_fields = ('recipe', 'ingredient',)
    empty_value_display = _('empty')
