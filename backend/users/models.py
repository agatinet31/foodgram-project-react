from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from api.settings import USER_ME
from users.settings import ADMIN, MODERATOR, USER, USER_ROLES


class CustomUser(AbstractUser):
    """Модель CustomUser управления пользователями."""
    first_name = models.CharField(
        _('first name'),
        max_length=150,
        help_text=_(
            'Required. Enter first name, please. 150 characters or fewer.'
        )
    )
    last_name = models.CharField(
        _('last name'),
        max_length=150,
        help_text=_(
            'Required. Enter last name, please. 150 characters or fewer.'
        )
    )
    email = models.EmailField(
        _('email'),
        max_length=254,
        unique=True,
        help_text=_(
            'Required. A valid email address, please. 254 characters or fewer.'
        ),
        validators=[EmailValidator],
        error_messages={
            'unique': _('A user with that email already exists.'),
        }
    )
    password = models.CharField(
        _('password'),
        max_length=150
    )
    role = models.CharField(
        max_length=50,
        choices=USER_ROLES,
        default=USER,
        verbose_name='Роль'
    )
    confirmation_code = models.BigIntegerField(
        default=0,
        verbose_name='Код подтверждения'
    )

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_powereduser(self):
        return self.role in [MODERATOR, ADMIN]

    class Meta(AbstractUser.Meta):
        ordering = ['username']

        constraints = [
            models.CheckConstraint(
                check=~models.Q(username__iexact=USER_ME),
                name="reserve_USER_ME"
            )
        ]

    def __str__(self):
        return self.email
