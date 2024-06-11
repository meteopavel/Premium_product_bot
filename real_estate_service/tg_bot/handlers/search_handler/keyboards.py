from telegram import InlineKeyboardButton
from telegram.ext import ContextTypes
from django.db import models

from object.models import (
    City,
)
from .constants import MAIN_FIELDS, OTHER_FIELDS
from .utils import dict_to_string


def main_keyboard(
        context:  ContextTypes.DEFAULT_TYPE
) -> list[list[InlineKeyboardButton]]:
    keyboard = []
    for field in MAIN_FIELDS:
        keyboard.append(
            [InlineKeyboardButton(MAIN_FIELDS[field], callback_data=field)]
        )
    is_search_data = False
    for field in MAIN_FIELDS | OTHER_FIELDS:
        if field in context.user_data and field != 'location__city':
            is_search_data = True
            break
    if is_search_data:
        keyboard.append(
            [
                InlineKeyboardButton('Очистить фильтры',
                                     callback_data='refresh_all'),
                InlineKeyboardButton('Прочее', callback_data='other'),
            ]
        )
        keyboard.append(
            [InlineKeyboardButton('Показать результат',
                                  callback_data='represent_results')]
        )
    else:
        keyboard.append(
            [
                InlineKeyboardButton('Прочее', callback_data='other'),
                InlineKeyboardButton('Показать результат',
                                     callback_data='represent_results')
            ]
        )
    return keyboard


def other_keyboard(
        context:  ContextTypes.DEFAULT_TYPE
) -> list[list[InlineKeyboardButton]]:
    keyboard = []
    for field in OTHER_FIELDS:
        keyboard.append(
            [InlineKeyboardButton(OTHER_FIELDS[field], callback_data=field)]
        )
    is_search_data = False
    for field in OTHER_FIELDS:
        if field in context.user_data:
            is_search_data = True
            break
    if is_search_data:
        keyboard.append(
            [
                InlineKeyboardButton(
                    'Сбросить', callback_data='refresh_other'),
                InlineKeyboardButton('Вернуться в меню',
                                     callback_data='return_to_main'),
            ]
        )
    else:
        keyboard.append(
            [
                InlineKeyboardButton('🟩 Вернуться в меню',
                                     callback_data='return_to_main'),
            ]
        )

    return keyboard


async def all_obj_keyboard(
        model: models.Model
) -> list[list[InlineKeyboardButton]]:
    keyboard = []
    async for object in model.objects.all().values_list('name', 'pk'):
        data = {
            'name': object[0],
            'pk': object[1]
        }
        keyboard.append(
            [
                InlineKeyboardButton(data['name'], callback_data=data['pk'])
            ]
        )
    keyboard.append(
        [InlineKeyboardButton('Вернутся в меню', callback_data='menu')]
    )
    return keyboard


async def location__city_keyboard() -> list[list[InlineKeyboardButton]]:
    """Создает клавиатуру из основных городов"""
    keyboard = []
    async for city in City.objects.filter(
        is_in_main_menu=True
    ).values_list('name', 'pk'):
        city_dic = {'name': city[0], 'pk': city[1]}
        keyboard.append(
            [
                InlineKeyboardButton(
                    city_dic['name'],
                    callback_data=city_dic['pk']
                )
            ]
        )
    keyboard.append([InlineKeyboardButton(
        'Города нет в списке. Выбрать другой.',
        callback_data='city_typing'
    )])
    return keyboard


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


async def send_citys_keyboard(
        citys: list[dict],
        page: int
) -> list[list[InlineKeyboardButton]]:
    start_index = page * 6
    end_index = start_index + 6
    items = citys[start_index:end_index]
    if not citys:
        keyboard = [
            [InlineKeyboardButton('выйти', callback_data='main_menu')],
            [InlineKeyboardButton(
                'попробовать еще', callback_data='city_typing')]
        ]
        return keyboard
    keyboard = []
    for city in items:
        keyboard.append(
            [InlineKeyboardButton(
                city['name'] + ':' + city['region'],
                callback_data=city['pk'])
             ]
        )
    keyboard.append([])
    if page > 0:
        keyboard[-1].append(InlineKeyboardButton(
            'Предыдущая', callback_data=f'page_{page-1}'))
    if end_index < len(citys):
        keyboard[-1].append(InlineKeyboardButton(
            'Следующая', callback_data=f'page_{page+1}'))
    keyboard.append(
        [InlineKeyboardButton('выйти', callback_data='main_menu')]
    )
    return keyboard


def send_page_keyboard(page, length):
    keyboard = []
    if page > 0:
        keyboard.append(InlineKeyboardButton(
            "Предыдущая", callback_data=f"page_{page-1}"))
    if page + 1 < length:
        keyboard.append(InlineKeyboardButton(
            "Следующая", callback_data=f"page_{page+1}"))
    keyboard.append(
        InlineKeyboardButton('выйти', callback_data='main_menu')
    )
    return [keyboard]
