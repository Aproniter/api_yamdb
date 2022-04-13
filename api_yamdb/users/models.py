from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE = (
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin'),
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]*$',
            message='Имя пользователя содержит недопустимые символы',
            code='invalid_username'
        ),
        ]
    )
    first_name = models.CharField(
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        blank=True
    )

    role = models.CharField(
        max_length=max(len(role) for role in ROLE),
        choices=ROLE,
        default=USER,
    )
    bio = models.TextField(
        blank=True,
        null=True,
    )

    email = models.EmailField(
        max_length=254,
        unique=True,
    )

    @property
    def is_admin(self):
        return self.is_staff or self.role == self.ADMIN

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
