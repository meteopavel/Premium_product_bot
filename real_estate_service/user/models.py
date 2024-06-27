from django.contrib.auth.models import AbstractUser
from django.db import models

from user import constants


class User(AbstractUser):

    username = models.CharField(
        verbose_name="Имя пользователя",
        max_length=constants.MAX_USERNAME_LENGTH,
        unique=True,
    )
    email = models.EmailField(
        verbose_name="Электронная почта",
        max_length=constants.MAX_EMAIL_LENGTH,
        unique=True,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ("username",)
        verbose_name = "Администратор"
        verbose_name_plural = "Администраторы"


class TelegramUser(models.Model):

    tg_id = models.BigIntegerField(
        verbose_name="Telegram id",
        unique=True,
    )
    first_name = models.CharField(
        verbose_name="Telegram first_name",
        max_length=constants.MAX_USERNAME_LENGTH,
    )
    last_name = models.CharField(
        verbose_name="Telegram lastname",
        max_length=constants.MAX_USERNAME_LENGTH,
        blank=True,
    )
    username = models.CharField(
        verbose_name="Telegram username",
        max_length=constants.MAX_USERNAME_LENGTH,
        blank=True,
    )
    is_blocked = models.BooleanField(
        verbose_name="Заблокирован", default=False
    )
    created_at = models.DateTimeField(
        auto_now=True, verbose_name="Registration date"
    )

    search_parameters = models.TextField(
        verbose_name="Строка, хранящая поисковые парамерты",
        null=True,
        blank=True,
    )
    is_subscribed = models.BooleanField(
        verbose_name="Подписан на обновления", default=False
    )
    staff_user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="ID сотрудника",
        null=True,
        blank=True,
        related_name="tg_user",
    )

    class Meta:
        ordering = ("first_name",)
        verbose_name = "Пользователь Telegram"
        verbose_name_plural = "Пользователи Telegram"

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        if self.username:
            return self.username
        else:
            return self.tg_id


class ArhivedTelegramUser(models.Model):

    tg_id = models.BigIntegerField(
        verbose_name="Telegram id",
        unique=True,
    )
    is_blocked = models.BooleanField(
        verbose_name="Заблокирован", default=False
    )
    created_at = models.DateTimeField(
        verbose_name="Registration date"
    )

    search_parameters = models.TextField(
        verbose_name="Строка, хранящая поисковые парамерты",
        null=True,
        blank=True,
    )
    is_subscribed = models.BooleanField(
        verbose_name="Подписан на обновления", default=False
    )
    reviews = models.TextField(
        verbose_name="строка, хранящая отзывы пользователя"
    )
    favorites = models.TextField(
        verbose_name="строка, хранящая избранные обьявления"
    )
    arhived_at = models.DateTimeField(
        auto_now=True, verbose_name="Arhive date"
    )

    class Meta:
        verbose_name = "Архивный пользователь Telegram"
        verbose_name_plural = "Архивный пользователи Telegram"

    def __str__(self):
        return str(self.arhived_at)
