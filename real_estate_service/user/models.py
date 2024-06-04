from django.contrib.auth.models import AbstractUser
from django.db import models

from user import constants


class User(AbstractUser):

    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=constants.MAX_USERNAME_LENGTH,
        unique=True,
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=constants.MAX_EMAIL_LENGTH,
        unique=True,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Администратор'
        verbose_name_plural = 'Администраторы'


class TelegramUser(models.Model):

    tg_id = models.PositiveIntegerField(
        verbose_name='Telegram id',
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='Telegram first_name',
        max_length=constants.MAX_USERNAME_LENGTH,
    )
    last_name = models.CharField(
        verbose_name='Telegram lastname',
        max_length=constants.MAX_USERNAME_LENGTH,
        blank=True
    )
    username = models.CharField(
        verbose_name='Telegram username',
        max_length=constants.MAX_USERNAME_LENGTH,
        blank=True
    )
    created_at = models.DateTimeField(auto_now=True, verbose_name='Registration date')

    class Meta:
        ordering = ('first_name',)
        verbose_name = 'Пользователь Telegram'
        verbose_name_plural = 'Пользователи Telegram'
