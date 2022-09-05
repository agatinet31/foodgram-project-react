from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    validate_slug)
from django.db import models

from reviews.validators import validation_year
from users.models import CustomUser


class TextPubDateModel(models.Model):
    """Абстрактная модель. Добавляет дату создания и автора к тексту."""
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='%(class)ss',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления'
    )
    text = models.TextField(
        verbose_name='Текст'
    )

    class Meta:
        """Метаданые абстрактной модели."""
        abstract = True
        ordering = ('-pub_date',)


class SlugDataModel(models.Model):
    """Абстрактная Slug модель."""
    name = models.CharField(
        unique=True,
        max_length=256,
        verbose_name='Наименование'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        validators=[validate_slug],
        verbose_name='Слаг'
    )

    class Meta:
        """Метаданые абстрактной модели."""
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(SlugDataModel):
    """Модель категорий."""
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )

    class Meta(SlugDataModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(SlugDataModel):
    """Модель жанров."""
    class Meta(SlugDataModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель произведений."""
    name = models.CharField(
        max_length=200,
        verbose_name='Наименование'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="titles",
        blank=True,
        null=True,
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр'
    )
    year = models.SmallIntegerField(
        db_index=True,
        validators=[validation_year],
        verbose_name='Год публикации'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return (
            f'ID: {self.id}; Name: "{self.name[:15]}"; '
            f'Published: "{self.year}"'
        )


class Review(TextPubDateModel):
    """Модель отзывов."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    score = models.PositiveSmallIntegerField(
        default=5,
        validators=[
            MaxValueValidator(10, 'Максимально значение рейтинга 10'),
            MinValueValidator(1, 'Минимальное значение рейтинга 1')
        ],
        verbose_name='Рейтинг'
    )

    class Meta(TextPubDateModel.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [models.UniqueConstraint(
            fields=('author', 'title',),
            name='unique_review'
        )]

    def __str__(self):
        return (
            f'ID: {self.id}; Author: "{self.author.username}"; '
            f'Text: "{self.text[:15]}"; Score: "{self.score}"; '
            f'Created: "{self.pub_date}"'
        )


class Comment(TextPubDateModel):
    """Модель комментариев."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )

    class Meta(TextPubDateModel.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return (
            f'ID: {self.id}; Author: "{self.author.username}"; '
            f'Text: "{self.text[:15]}"; Created: "{self.pub_date}"; '
            f'Review ID: "{self.review.id}"'
        )
