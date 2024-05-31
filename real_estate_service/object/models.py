import uuid

from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import ArrayField

PHONE_REGEX = r'^\+?1?\d{9,15}$'
PHONE_NUMBER_FIELD_MAX_LENTH = 17
SHORT_CAHR_FIELD_MAX_LENGTH = 100
LONG_CAHR_FIELD_MAX_LENGTH = 256
FAREST_WEST_TIMEZONE = -1
FAREST_EAST_TIMEZONE = 9


class City(models.Model):
    name = models.CharField(max_length=SHORT_CAHR_FIELD_MAX_LENGTH)
    time_zone_uts = models.IntegerField(
        verbose_name='Временная зона UTS',
        validators=[
            MinValueValidator(FAREST_WEST_TIMEZONE),
            MaxValueValidator(FAREST_EAST_TIMEZONE)
        ]
    )

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name


class PhoneNumberField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['validators'] = [RegexValidator(regex=PHONE_REGEX)]
        kwargs['max_length'] = PHONE_NUMBER_FIELD_MAX_LENTH
        kwargs['blank'] = True
        super().__init__(*args, **kwargs)


class BaseModel(models.Model):
    name = models.CharField(
        max_length=SHORT_CAHR_FIELD_MAX_LENGTH,
        verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Category(BaseModel):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class BuldingType(BaseModel):
    class Meta:
        verbose_name = 'Тип здания'
        verbose_name_plural = 'Типы здания'


class Condition(BaseModel):
    class Meta:
        verbose_name = 'Состояние помещений'
        verbose_name_plural = 'Состояния помещений'


class Contact(BaseModel):
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name='Эл. почта'
    )
    phone_number = PhoneNumberField(
        blank=True,
        null=True,
        verbose_name='Номер телефона'
    )

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'


class Realty(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True
    )
    title = models.CharField(
        max_length=SHORT_CAHR_FIELD_MAX_LENGTH,
        verbose_name='Название'
    )
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        verbose_name='Город',
        null=True
    )
    address = models.CharField(
        max_length=LONG_CAHR_FIELD_MAX_LENGTH,
        verbose_name='Адрес',
        null=True
    )
    email = models.EmailField(blank=True, null=True, verbose_name='Эл. почта')
    site = models.URLField(blank=True, null=True, verbose_name='Сайт')
    contact = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        verbose_name='Контакт',
        related_name='realtys',
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        blank=True,
        null=True
    )
    area = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Площадь, метры квадратные'
    )
    price = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Цена, рублей в месяц за квадратный метр'
    )
    publish_date = models.DateField(auto_now_add=True)
    condition = models.ForeignKey(
        Condition,
        on_delete=models.SET_NULL,
        verbose_name='Состояние помещения',
        blank=True,
        null=True
    )
    building_type = models.ForeignKey(
        BuldingType,
        on_delete=models.SET_NULL,
        verbose_name='Тип здания',
        blank=True,
        null=True
    )
    text = models.TextField(
        verbose_name='Текст обьявления',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return f'Объект {self.title} в городе {self.city.name}'
