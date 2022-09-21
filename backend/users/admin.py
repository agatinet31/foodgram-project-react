from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from users.models import CustomUser, Subscriber


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Класс определяющий настройки кастомной модели User в админке."""
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'first_name',
                'last_name',
                'email',
                'password1',
                'password2',
            ),
        }),
    )
    list_filter = ('username', 'email',)


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    """Конфигурация для модели Subscriber в админке."""
    list_display = ('user', 'author', 'date_subscriber')
    list_filter = ('user', 'author',)
    search_fields = ('user', 'author',)
    empty_value_display = _('empty')
