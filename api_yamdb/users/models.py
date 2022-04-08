from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    """Проверьте, соответствуют ли 
    размеры полей у класса-родителя размеру полей из ТЗ (Redoc). 
    Учтите версию Django, которая используется в проекте.
    !!! Изменил размер поля и добавил валидацию username
    """
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
        blank=False,
        null=False,
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
        max_length=150,
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
        blank=False,
        null=False
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
