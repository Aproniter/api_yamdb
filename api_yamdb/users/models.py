from django.db import models
from django.contrib.auth.models import AbstractUser


USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
ROLE = (
    (USER, 'User'),
    (MODERATOR, 'Moderator'),
    (ADMIN, 'Admin'),
)


class User(AbstractUser):
    username = models.CharField(
        max_length=80,
        unique=True,
        blank=False,
        null=False
    )
    email = models.EmailField(
        max_length=80,
        unique=True,
        blank=False,
        null=False
    )
    role = models.CharField(
        'Роль',
        max_length=20,
        choices=ROLE,
        default=USER,
        blank=True
    )
    bio = models.TextField(
        'биография',
        blank=True,
    )
    first_name = models.CharField(
        'Имя',
        max_length=80,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=80,
        blank=True
    )
    father_name = models.CharField(
        'Отчество',
        max_length=80,
        blank=True
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=4,
        null=True,
        blank=False,
        default='0000'
    )

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
