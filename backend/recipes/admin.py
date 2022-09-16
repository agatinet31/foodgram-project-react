from django.contrib import admin
from django.template.loader import get_template
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Конфигурация для модели Tag в админке."""
    list_display = ('name', 'slug', 'color',)
    list_editable = ('color',)
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


class RecipeIngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Конфигурация для модели Recipe в админке."""
    list_display = ('name', 'author',)
    list_filter = ('author', 'name', 'tags')
    search_fields = ('name',)
    filter_horizontal = ('tags', 'favorites', 'shopping_carts',)
    inlines = (RecipeIngredientInline,)
    readonly_fields = ('image_tag', 'ingredients_inline', 'amount_favorites',)
    empty_value_display = _('empty')
    fields = (
        'name',
        'author',
        'pub_date',
        'image_tag',
        'image',
        'cooking_time',
        'ingredients_inline',
        'text',
        'tags',
        'amount_favorites',
        'favorites',
        'shopping_carts'
    )

    def has_add_permission(self, request):
        """Запрет добавления рецепта в админке."""
        return False

    def amount_favorites(self, recipe):
        return recipe.favorites.count()

    amount_favorites.short_description = _('amount_favorites')

    def image_tag(self, recipe):
        if recipe.image:
            return mark_safe(
                f'<img src="{recipe.image.url}" height="300" />'
            )
        return None

    image_tag.short_description = _('image')

    image_tag.allow_tags = True

    def ingredients_inline(self, obj=None, *args, **kwargs):
        context = getattr(self.response, 'context_data', None) or {}
        inline = context['inline_admin_formset'] = context['inline_admin_formsets'].pop(0)
        return get_template(inline.opts.template).render(context, self.request)

    ingredients_inline.short_description = _('ingredients')

    def render_change_form(self, request, *args, **kwargs):
        self.request = request
        self.response = super().render_change_form(request, *args, **kwargs)
        return self.response


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    """Конфигурация для модели RecipeIngredient в админке."""
    list_display = ('recipe', 'ingredient', 'amount')
    list_filter = ('recipe', 'ingredient',)
    search_fields = ('recipe', 'ingredient',)
    empty_value_display = _('empty')
