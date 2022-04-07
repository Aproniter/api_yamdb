from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User


class Category(models.Model):
    name = models.CharField(
        'Категория',
        max_length=200
    )
    slug = models.SlugField(
        unique=True,
        db_index=True
    )

    def __str__(self):
        return f'{self.name} {self.name}'


class Genre(models.Model):
    name = models.CharField(
        'Жанр',
        max_length=200
    )
    slug = models.SlugField(
        'cлаг жанра',
        unique=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return f'{self.name} {self.name}'


class Title(models.Model):
    name = models.CharField(
        'Название',
        max_length=200,
        db_index=True
    )
    year = models.IntegerField(
        'год',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        blank=True
    )
    description = models.TextField(
        'Описание',
        max_length=255,
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.CharField(
        max_length=200
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.IntegerField(
        'Оценка',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        ),
        error_messages={'validators': 'Оценка от 1 до 10!'}
    )
    pub_date = models.DateTimeField(
        'дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author', ),
                name='unique review'
            )]
        ordering = ('pub_date',)

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.CharField(
        max_length=500
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return self.text
