from telegram import InlineKeyboardButton
from django.db import models
from object.models import (
    City,
)
from .constants import MAIN_FIELDS, OTHER_FIELDS


def main_keyboard() -> list[list[InlineKeyboardButton]]:
    keyboard = []
    for field in MAIN_FIELDS:
        keyboard.append(
            [InlineKeyboardButton(MAIN_FIELDS[field], callback_data=field)]
        )
    keyboard.append(
        [
            InlineKeyboardButton('Очистить фаильтры',
                                 callback_data='refresh_all'),
            InlineKeyboardButton('Прочее', callback_data='other'),
        ]
    )
    keyboard.append(
        [InlineKeyboardButton('Показать результат',
                              callback_data='represent_results')]
    )
    return keyboard


def other_keyboard() -> list[list[InlineKeyboardButton]]:
    keyboard = []
    for field in OTHER_FIELDS:
        keyboard.append(
            [InlineKeyboardButton(OTHER_FIELDS[field], callback_data=field)]
        )
    keyboard.append(
        [
            InlineKeyboardButton(
                'Сбросить', callback_data='refresh_other'),
            InlineKeyboardButton('Вернуться в меню',
                                 callback_data='return_to_main'),
        ]
    )
    return keyboard


async def all_obj_keyboard(
        model: models.Model
) -> list[list[InlineKeyboardButton]]:
    keyboard = []
    async for category in model.objects.all().values_list('name', flat=True):
        keyboard.append(
            [
                InlineKeyboardButton(category, callback_data=category)
            ]
        )
    keyboard.append(
        [InlineKeyboardButton('Вернутся в меню', callback_data='menu')]
    )
    return keyboard


async def city_keyboard() -> list[list[InlineKeyboardButton]]:
    keyboard = []
    async for city in City.objects.all().values_list('name', flat=True):
        keyboard.append(
            [
                InlineKeyboardButton(city, callback_data=city)
            ]
        )
    keyboard.append([InlineKeyboardButton(
        'Города нет в списке. Выбрать другой.',
        callback_data='other_city'
    )])
    return keyboard

OTHER_CITY_KEYBOARD = [
    [InlineKeyboardButton(
        'Какойто город', callback_data='выбрал-Какойто город')],
]

AREA_KEYBOARD = [
    [InlineKeyboardButton('1-150', callback_data='1-150')],
    [InlineKeyboardButton(
        '150-1000', callback_data='150-1000')],
    [InlineKeyboardButton('1000-100000', callback_data='1000-100000')]
]

PRICE_KEYBOARD = [
    [InlineKeyboardButton('1-150', callback_data='1-150')],
    [InlineKeyboardButton(
        '150-1000', callback_data='150-1000')],
    [InlineKeyboardButton('1000-100000', callback_data='1000-100000')]
]


REPRESENT_RESULTS_KEYBOARD = [
    [InlineKeyboardButton('Посмотрел', callback_data='Посмотрел')],
]

PUBLISH_DATE_KEYBOARD = [
    [InlineKeyboardButton('Сегодняшние', callback_data='1')],
    [InlineKeyboardButton(
        'За неделю', callback_data='7')],
    [InlineKeyboardButton(
        'За месяц', callback_data='31')],
    [InlineKeyboardButton('Полгода', callback_data='184')]
]
