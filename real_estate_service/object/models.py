from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models
from django.db.models import Q

PHONE_REGEX = r"^\+?1?\d{9,15}$"
PHONE_NUMBER_FIELD_MAX_LENTH = 17
SHORT_CAHR_FIELD_MAX_LENGTH = 200
LONG_CAHR_FIELD_MAX_LENGTH = 256
FAREST_WEST_TIMEZONE = -12
FAREST_EAST_TIMEZONE = 14
MAX_INTERVALS_COUNT = 7


class Country(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

    def __str__(self):
        return self.title


class City(models.Model):
    name = models.CharField(
        max_length=SHORT_CAHR_FIELD_MAX_LENGTH, verbose_name="Название"
    )
    time_zone_uts = models.IntegerField(
        verbose_name="Временная зона UTS",
        validators=[
            MinValueValidator(FAREST_WEST_TIMEZONE),
            MaxValueValidator(FAREST_EAST_TIMEZONE),
        ],
        null=True,
        blank=True,
    )
    country = models.ForeignKey(
        Country, verbose_name="Страна", on_delete=models.CASCADE
    )
    district = models.CharField(
        max_length=150, verbose_name="Область", null=True, blank=True
    )
    is_in_main_menu = models.BooleanField(
        verbose_name="Показать в основном меню", default=False
    )

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"

    def __str__(self):
        return f"{self.country} - {self.name}"


class PhoneNumberField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs["validators"] = [RegexValidator(regex=PHONE_REGEX)]
        kwargs["max_length"] = PHONE_NUMBER_FIELD_MAX_LENTH
        kwargs["blank"] = True
        super().__init__(*args, **kwargs)


class BaseModel(models.Model):
    name = models.CharField(
        max_length=SHORT_CAHR_FIELD_MAX_LENGTH, verbose_name="Название"
    )

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Category(BaseModel):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class BuldingType(BaseModel):
    class Meta:
        verbose_name = "Тип здания"
        verbose_name_plural = "Типы здания"


class Condition(BaseModel):
    class Meta:
        verbose_name = "Состояние помещений"
        verbose_name_plural = "Состояния помещений"


class Contact(BaseModel):
    email = models.EmailField(blank=True, null=True, verbose_name="Эл. почта")
    phone_number = ArrayField(
        base_field=PhoneNumberField(
            blank=True, null=True, verbose_name="Номер телефона"
        ),
        blank=True,
        null=True,
        verbose_name="Номера телефонов",
    )

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"


class Location(models.Model):
    city = models.ForeignKey(
        City, on_delete=models.PROTECT, verbose_name="Город"
    )
    post_index = models.CharField(
        max_length=10, verbose_name="Почтовый индекс", null=True, blank=True
    )
    street = models.CharField(max_length=200, verbose_name="Улица")
    building = models.CharField(max_length=60, verbose_name="Строение")
    floor = models.CharField(
        max_length=60, verbose_name="Этаж", null=True, blank=True
    )
    room = models.CharField(
        max_length=60, verbose_name="Помещение", null=True, blank=True
    )

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"

    def __str__(self):
        return f"Локация в {self.city}"


class Realty(models.Model):
    title = models.CharField(
        max_length=SHORT_CAHR_FIELD_MAX_LENGTH, verbose_name="Название"
    )
    image = models.ImageField(
        upload_to="realty/images/",
        verbose_name="Изображение",
        null=True,
        default=None,
    )
    location = models.ForeignKey(
        Location, verbose_name="Локация", on_delete=models.PROTECT, null=True
    )
    site = models.URLField(blank=True, null=True, verbose_name="Сайт")
    contact = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        verbose_name="Контакт",
        related_name="realtys",
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        blank=True,
        null=True,
    )
    area = models.PositiveIntegerField(
        blank=True, null=True, verbose_name="Площадь, метры квадратные"
    )
    price = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Цена, рублей в месяц за квадратный метр",
    )
    publish_date = models.DateField(auto_now_add=True)
    condition = models.ForeignKey(
        Condition,
        on_delete=models.SET_NULL,
        verbose_name="Состояние помещения",
        blank=True,
        null=True,
    )
    building_type = models.ForeignKey(
        BuldingType,
        on_delete=models.SET_NULL,
        verbose_name="Тип здания",
        blank=True,
        null=True,
    )
    text = models.TextField(
        verbose_name="Текст обьявления", blank=True, null=True
    )

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return self.title


class BaseIntervals(models.Model):
    minimum = models.PositiveIntegerField(
        blank=True, null=True, verbose_name="минимальное значение"
    )
    maximum = models.PositiveIntegerField(
        blank=True, null=True, verbose_name="максимальное значение"
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
