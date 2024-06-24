from django.db import models
from django.utils.translation import gettext_lazy as _

from object.models import Realty
from user.models import TelegramUser


class Review(models.Model):
    class ReviewStatus(models.TextChoices):
        PENDING = "P", _("Pending")
        APPROVED = "A", _("Approved")
        REJECTED = "R", _("Rejected")

    author = models.ForeignKey(
        TelegramUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name = "Автор"
    )
    real_estate = models.ForeignKey(
        Realty,
        related_name="reviews",
        on_delete=models.CASCADE,
        verbose_name = "Объявление"
        
    )
    text = models.TextField(verbose_name = "Текст")
    status = models.CharField(
        max_length=1,
        choices=ReviewStatus.choices,
        default=ReviewStatus.PENDING,
        verbose_name = "Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        if self.author:
            return f"Review by {self.author} for {self.real_estate}"
        else:
            return f"Review for {self.real_estate}"
