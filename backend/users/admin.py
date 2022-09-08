from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from users.forms import CustomUserChangeForm, CustomUserCreationForm
from users.models import CustomUser, Subscriber


class SubscribersInlineAdmin(admin.TabularInline):
    model = CustomUser.subscribed.through
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    """Класс определяющий настройки кастомной модели User в админке."""
    # inlines = (SubscribersInlineAdmin,)
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    fieldsets = (
        (None, {
            'fields': (
                'username',
                'password'
            )
        }
        ),
        (_('Personal info'), {
            'fields': (
                'first_name',
                'last_name',
                'email'
            )
        }),
        (_('Subscribed / Subscribers'), {
            'fields': (
                'subscribed',
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            ),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )    
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
    # autocomplete_fields = ('subscribed',)
    filter_horizontal = ('subscribed', )
    list_display = ('username', 'first_name', 'last_name', 'email', )
    list_filter = ('username', 'first_name', 'last_name', 'email',)


admin.site.register(CustomUser, CustomUserAdmin)

"""

        (_('Subscribed / Subscribers'), {
            'fields': (
                'subscribed',
                'subscribers'
            )
        }),

    filter_horizontal = ('subscribed', 'subscribers')
"""
