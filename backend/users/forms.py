from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрациия пользователя."""
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'bio', 'role', 'confirmation_code')


class CustomUserChangeForm(UserChangeForm):
    """Форма изменения данных пользователя."""
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'bio', 'role', 'confirmation_code')
