from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q

from object.models import SHORT_CAHR_FIELD_MAX_LENGTH

MAX_INTERVALS_COUNT = 7

class BaseIntervals(models.Model):
    minimum = models.PositiveIntegerField(
        blank=True, null=True, verbose_name="Минимальное значение"
    )
    maximum = models.PositiveIntegerField(
        blank=True, null=True, verbose_name="Максимальное значение"
    )

    class Meta:
        verbose_name = "Интервал"
        verbose_name_plural = "Интервалы"
        constraints = [
            models.CheckConstraint(
                check=Q(minimum__lte=models.F("maximum")),
                name="minimum_lte_maximum",
            )
        ]
        ordering = ["minimum"]
        abstract = True

    def clean(self):
        if (
            self.maximum is not None
            and self.minimum is not None
            and self.maximum <= self.minimum
        ):
            raise ValidationError("Max price must be greater than min price.")

    def __str__(self):
        return f"{self.minimum}-{self.maximum}"


class PriceIntervals(BaseIntervals):
    class Meta:
        verbose_name = "Интервал цен"
        verbose_name_plural = "Интервалы цен"

    def save(self, *args, **kwargs):
        if PriceIntervals.objects.count() >= MAX_INTERVALS_COUNT:
            raise ValidationError(
                f"Only up to {MAX_INTERVALS_COUNT} Price Intervals are allowed."  # noqa
            )
        super().save(*args, **kwargs)


class AreaIntervals(BaseIntervals):
    class Meta:
        verbose_name = "Интервал площади"
        verbose_name_plural = "Интервалы площади"

    def save(self, *args, **kwargs):
        if AreaIntervals.objects.count() >= MAX_INTERVALS_COUNT:
            raise ValidationError(
                f"Only up to {MAX_INTERVALS_COUNT} Area Intervals are allowed."
            )
        super().save(*args, **kwargs)
   
        
class DateInterval(models.Model):
    name = models.CharField(
        max_length=SHORT_CAHR_FIELD_MAX_LENGTH,
        verbose_name="Название периода"
    )
    date_interval = models.SmallIntegerField(
        verbose_name="количество дней от текущей даты"
    )
    class Meta:
        ordering = ["date_interval"]
        verbose_name = "Интервал дней"
        verbose_name_plural = "Интервалы дней"

    def __str__(self):
        return self.name