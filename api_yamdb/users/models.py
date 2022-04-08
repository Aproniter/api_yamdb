from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Проверьте, соответствуют ли размеры полей у класса-родителя размеру полей из ТЗ (Redoc). Учтите версию Django, которая используется в проекте."""
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
        blank=True,
        null=True,
    )
    token = models.CharField(
        max_length=1000,
        blank=True,
        null=True
    )
    """Лишнее поле"""
    email = models.EmailField(
        max_length=254,
        unique=True,
    )
    confirm_code = models.CharField(
        max_length=6,
        blank=True,
        null=True,
    )
    """А зачем его хранить в базе?"""

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_admin(self):
        return self.role == self.ADMIN
    """Пропускаются админы со стороны джанго - is_staff"""

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
