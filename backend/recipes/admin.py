from django.contrib import admin
from django.template.loader import get_template
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

from recipes.models import Ingredient, Recipe, Tag


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
    """Класс inline для ингридиентов рецепта."""
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

    class Media:
        """Media класс кастомизации прорисовки рецепта в админке."""
        css = {
            'all': ('recipes/css/admin.css', )
        }

    def has_add_permission(self, request):
        """Запрет добавления рецепта в админке."""
        return False

    def amount_favorites(self, recipe):
        """Общее число добавлений в избранное."""
        return recipe.favorites.count()

    amount_favorites.short_description = _('amount_favorites')

    def image_tag(self, recipe):
        """Прорисовка изображения рецепта."""
        if recipe.image:
            return mark_safe(
                f'<img src="{recipe.image.url}" height="300" />'
            )
        return None

    image_tag.short_description = _('image')

    image_tag.allow_tags = True

    def ingredients_inline(self, obj=None, *args, **kwargs):
        """Измение положения inline."""
        context = getattr(self.response, 'context_data', None) or {}
        inline_admin_form = context['inline_admin_formsets'].pop(0)
        inline = context['inline_admin_formset'] = inline_admin_form
        return get_template(inline.opts.template).render(context, self.request)

    ingredients_inline.short_description = _('ingredients')

    def render_change_form(self, request, *args, **kwargs):
        """Рендер формы редактирования рецепта."""
        self.request = request
        self.response = super().render_change_form(request, *args, **kwargs)
        return self.response


@admin.register(Recipe.favorites.through)
class RecipeFavoritesAdmin(admin.ModelAdmin):
    """Конфигурация для `Избранного` в админке."""
    list_display = ('customuser', 'recipe',)
    list_filter = ('customuser__username', 'recipe__name')
    search_fields = ('customuser__username', 'recipe__name',)
    empty_value_display = _('empty')

    def __init__(self, *args, **kwargs):
        """Инициализация through модели избранного."""
        admin.ModelAdmin.__init__(self, *args, **kwargs)
        self.opts.verbose_name = _('favorite')
        self.opts.verbose_name_plural = _('favorites')
        self.opts.get_field('customuser').verbose_name = _('user')
        self.opts.get_field('recipe').verbose_name = _('recipe')


@admin.register(Recipe.shopping_carts.through)
class RecipeShoppingcartsAdmin(admin.ModelAdmin):
    """Конфигурация для `Список покупок` в админке."""
    list_display = ('customuser', 'recipe',)
    list_filter = ('customuser__username', 'recipe__name')
    search_fields = ('customuser__username', 'recipe__name',)
    empty_value_display = _('empty')

    def __init__(self, *args, **kwargs):
        """Инициализация through модели списка покупок."""
        admin.ModelAdmin.__init__(self, *args, **kwargs)
        self.opts.verbose_name = _('shopping_cart')
        self.opts.verbose_name_plural = _('shopping_carts')
        self.opts.get_field('customuser').verbose_name = _('user')
        self.opts.get_field('recipe').verbose_name = _('recipe')


admin.site.site_title = _('Аdministration Foodgram')
admin.site.site_header = _('Аdministration Foodgram')
