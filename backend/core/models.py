from django.db import models


class PubDateModel(models.Model):
    """Абстрактная модель. Добавляет дату создания."""
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    edit_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата редактирования'
    )

    class Meta:
        """Метаданые абстрактной модели."""
        abstract = True
