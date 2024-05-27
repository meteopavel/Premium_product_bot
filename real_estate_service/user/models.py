from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from user.validators import validate_username


class User(AbstractUser):

    SUPERADMIN = 'superadmin'
    ADMIN = 'admin'
    USER = 'user'

    ROLES = (
        (SUPERADMIN, 'Суперадминистратор'),
        (ADMIN, 'Администратор'),
        (USER, 'Пользователь'),
    )

    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=settings.MAX_USERNAME_LENGTH,
        unique=True,
        validators=(validate_username,)
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=settings.MAX_ROLE_LENGHT,
        choices=ROLES,
        default=USER
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=settings.MAX_EMAIL_LENGTH,
        unique=True
    )
    telegram_id = models.PositiveIntegerField(
        verbose_name='Telegram ID',
        unique=True,
        default=1
    )
    telegram_username = models.CharField(
        verbose_name='Telegram username',
        max_length=settings.MAX_USERNAME_LENGTH,
    )
    telegram_firstname = models.CharField(
        verbose_name='Telegram firstname',
        max_length=settings.MAX_USERNAME_LENGTH,
    )
    telegram_lastname = models.CharField(
        verbose_name='Telegram lastname',
        max_length=settings.MAX_USERNAME_LENGTH,
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
