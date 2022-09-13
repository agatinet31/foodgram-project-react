from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.utils import is_not_empty_query
from core.validators import validate_only_letters
from users.settings import USER_ME


class CustomUser(AbstractUser):
    """Модель CustomUser управления пользователями."""
    first_name = models.CharField(
        _('first name'),
        max_length=150,
        validators=[validate_only_letters],
        help_text=_(
            'Required. Enter first name, please. '
            '150 characters or fewer. Letters only.'
        ),
    )
    last_name = models.CharField(
        _('last name'),
        max_length=150,
        validators=[validate_only_letters],
        help_text=_(
            'Required. Enter last name, please. '
            '150 characters or fewer. Letters only.'
        ),
    )
    email = models.EmailField(
        _('email'),
        max_length=254,
        unique=True,
        validators=[EmailValidator],
        help_text=_(
            'Required. A valid email address, please. '
            '254 characters or fewer. Letters, digits and @/./+/-/_ only.'
        ),
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
        verbose_name=_('subscribed'),
        blank=True,
        symmetrical=False,
        through='Subscriber',
        through_fields=('user', 'author'),
        related_name='my_subscribers',
        help_text=_('Subscribed for this user.'),
    )
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    class Meta(AbstractUser.Meta):
        ordering = ['username']
        constraints = [
            models.CheckConstraint(
                check=~models.Q(username__iexact=USER_ME),
                name="reserve_USER_ME"
            ),
        ]

    @property
    def is_subscribed(self):
        """Проверка наличия подписок на авторов."""
        return is_not_empty_query(self.subscribed)

    def clean(self):
        """Валидация модели."""
        if self.username.upper() == USER_ME:
            raise ValidationError(
                {
                    'username':
                    _('The ME username is reserved. Specify another please.')
                }
            )
        super().clean()

    def __str__(self):
        """Вывод данных пользователя."""
        return f'{self.username} ({self.get_full_name()}), email: {self.email}'


class Subscriber(models.Model):
    """Модель подписчика на авторов."""
    user = models.ForeignKey(
        CustomUser,
        verbose_name=_('user'),
        on_delete=models.CASCADE,
        related_name='user_subscribers',
    )
    author = models.ForeignKey(
        CustomUser,
        verbose_name=_('author'),
        on_delete=models.CASCADE,
        related_name='author_subscribers',
    )
    date_subscriber = models.DateTimeField(
        _('date subscriber'),
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        """Метаданные модели подписчиков."""
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_user_author_subscriber'
            ),
            models.CheckConstraint(
                check=~models.Q(user_id=models.F('author_id')),
                name='check_not_loop_user_author'
            ),
        ]
        verbose_name = _('subscriber')
        verbose_name_plural = _('subscribers')

    def clean(self):
        """Валидация модели."""
        if self.user == self.author:
            raise ValidationError({'author': _('User cannot follow himself.')})

    def __str__(self):
        """Вывод подписчика и автора."""
        return f'{self.user.username}:{self.author.username}'
