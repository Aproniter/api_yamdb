from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE = (
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin'),
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE,
        default=USER,
    )
    bio = models.TextField(
        max_length=300,
        blank=True,
        null=True,
    )
    password = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    token = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )
    email = models.EmailField(
        max_length=254,
    )
    confirm_code = models.CharField(
        max_length=6,
        blank=True,
        null=True,
    )

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
