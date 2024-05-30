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
        unique=True
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class TelegramUser(models.Model):

    id = models.PositiveIntegerField(
        primary_key=True,
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
    )
    username = models.CharField(
        verbose_name='Telegram username',
        max_length=constants.MAX_USERNAME_LENGTH,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ('first_name',)
        verbose_name = 'Пользователь Telegram'
        verbose_name_plural = 'Пользователи Telegram'
