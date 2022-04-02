from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ANON = 'anon'
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE = (
        (ANON, 'Anonim'),
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin'),
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE,
        default=ANON
    )
