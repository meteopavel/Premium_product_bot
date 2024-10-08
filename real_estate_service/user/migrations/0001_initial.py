# Generated by Django 5.0.6 on 2024-06-12 06:42

import django.contrib.auth.models
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="TelegramUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "tg_id",
                    models.PositiveIntegerField(
                        unique=True, verbose_name="Telegram id"
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        max_length=150, verbose_name="Telegram first_name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True,
                        max_length=150,
                        verbose_name="Telegram lastname",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        blank=True,
                        max_length=150,
                        verbose_name="Telegram username",
                    ),
                ),
                (
                    "is_blocked",
                    models.BooleanField(
                        default=False, verbose_name="Заблокирован"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Registration date"
                    ),
                ),
            ],
            options={
                "verbose_name": "Пользователь Telegram",
                "verbose_name_plural": "Пользователи Telegram",
                "ordering": ("first_name",),
            },
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "password",
                    models.CharField(max_length=128, verbose_name="password"),
                ),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text=("Designates that this user has all permiss"
                                   "ions without explicitly assigning them."),
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text=("Designates whether the user can "
                                   "log into this admin site."),
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text=("Designates whether this user"
                                   " should be treated as active. Unselect "
                                   "this instead of deleting accounts."),
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="date joined",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        max_length=150,
                        unique=True,
                        verbose_name="Имя пользователя",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True,
                        max_length=254,
                        null=True,
                        unique=True,
                        verbose_name="Электронная почта",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text=("The groups this user belongs to. "
                                   "A user will get all permissions granted "
                                   "to each of their groups."),
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "Администратор",
                "verbose_name_plural": "Администраторы",
                "ordering": ("username",),
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
