from django.db import models
from django.db.models import UniqueConstraint
from object.models import Realty
from user.models import TelegramUser


class Favorite(models.Model):
    realty = models.ForeignKey(
        Realty,
        verbose_name="избранное",
        related_name="favorites",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        TelegramUser,
        verbose_name="пользователь",
        related_name="favorites",
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["user", "realty"], name="user_favorite_unique"
            )
        ]
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"

    def __str__(self):
        return f"{self.user} - {self.realty}"
