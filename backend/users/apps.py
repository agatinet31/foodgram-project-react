from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    """Класс конфигурирующий приложение users."""
    name = 'users'
    verbose_name = _('users')
