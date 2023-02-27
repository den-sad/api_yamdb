from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    )


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=255
    )
    year = models.IntegerField(
        verbose_name='Год выхода',
        max_length=4
    )
    rating = models.IntegerField(
        verbose_name='Рейтинг',
        default=None
    )
    description = models.TextField(
        verbose_name='Краткое описание',
        blank=True
    )
    genre = models.ForeignKey(
        'Genre',
        verbose_name='Жанр',
        on_delete=models.SET_NULL,
        related_name='titles'
    )
    category = models.ForeignKey(
        'Category',
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles'
    )

    def __str__(self):
        return self.name
