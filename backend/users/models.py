from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from api.settings import USER_ME


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
    subscribed = models.ManyToManyField(
        'self',
        related_name='subscribers',
        blank=True,
        symmetrical=False
    )

    class Meta(AbstractUser.Meta):
        ordering = ['username']

        constraints = [
            models.CheckConstraint(
                check=~models.Q(username__iexact=USER_ME),
                name="reserve_USER_ME"
            )
        ]

    def __str__(self):
        return f'{self.username} ({self.get_full_name()}), email: {self.email}'
