from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """Класс определяющий настройки кастомной модели User в админке."""
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    fieldsets = (
        (None, {
            'fields': (
                'username',
                'password',
                'role',
                'confirmation_code'
            )
        }
        ),
        (_('Personal info'), {
            'fields': (
                'first_name',
                'last_name',
                'email',
                'bio'
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
                'password1',
                'password2',
                'role',
                'email',
            ),
        }),
    )
    list_display = ('username', 'email', 'role', 'confirmation_code',)
    list_filter = ('username', 'email', 'role',)


admin.site.register(CustomUser, CustomUserAdmin)
