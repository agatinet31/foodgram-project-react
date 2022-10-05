from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.utils import is_exists_user_info
from core.validators import validate_only_letters
from users.settings import USER_ME


class CustomUserManager(BaseUserManager):
    def create_user(
        self, email, username, first_name, last_name, password=None
    ):
        """
        Создает и сохраняет пользователя с обязательными полями:
        email, username, first_name, last_name и password.
        """
        if not email:
            raise ValueError(_('Users must have an email address'))
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, username, first_name, last_name, password=None
    ):
        """
        Создает и сохраняет суперпользователя с обязательными полями:
        email, username, first_name, last_name и password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


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
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta(AbstractUser.Meta):
        ordering = ['username']
        constraints = [
            models.CheckConstraint(
                check=~models.Q(username__iexact=USER_ME),
                name="reserve_USER_ME"
            ),
        ]

    @property
    def is_admin(self):
        """Проверка административных прав у пользователя."""
        return self.is_staff or self.is_superuser

    def is_subscribed(self, author):
        """Проверка наличия подписок на автора."""
        return is_exists_user_info(self.subscribed, author)

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
        ordering = ['-date_subscriber']
        verbose_name = _('subscriber')
        verbose_name_plural = _('subscribers')

    def clean(self):
        """Валидация модели."""
        if self.user == self.author:
            raise ValidationError({'author': _('User cannot follow himself.')})

    def __str__(self):
        """Вывод подписчика и автора."""
        return f'{self.user.username}:{self.author.username}'
