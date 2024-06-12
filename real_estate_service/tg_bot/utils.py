import os
from datetime import datetime, timedelta

from django.db.models import Model
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv

from user.models import TelegramUser
from object.models import Realty
from tg_bot.handlers.search_handler.utils import string_to_dict
load_dotenv()

search_fields: list[str] = [
    'location__city', 'area', 'price', 'category',
    'publish_date', 'condition', 'building_type', 'text'
]
foregin_fields = ['location__city', 'category', 'condition', 'building_type',]
integer_fields = ['area', 'price']
datetime_field = 'publish_date'
text_field = 'text'


async def send_message_to_subscribers2(instance: Realty, chat_id):
    bot_token = os.getenv('TELEGRAM_TOKEN')
    bot = Bot(token=bot_token)
    async for user in TelegramUser.objects.filter(is_subscribed=True):
        is_sutable = True
        search_parameters = string_to_dict(user.search_parameters)
        instance_values = get_filled_fields(instance, search_parameters)
        for field in foregin_fields:
            if field in instance_values and not search_parameters[field] == instance_values[field]:
                is_sutable = False
        for field in integer_fields:
            if field in instance_values:
                minimum = search_parameters[field].split('-')[0]
                maximum = search_parameters[field].split('-')[1]
                if instance_values[field] > maximum and instance_values[field] <= minimum:
                    is_sutable = False
        if text_field in instance_values:
            if not search_parameters[text_field] in instance_values[text_field]:
                is_sutable = False
        if is_sutable:
            keyboard = [
                [
                    InlineKeyboardButton(
                        f'{instance.title}',
                        callback_data=f'realty_{instance.pk}'
                    )
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await bot.send_message(
                chat_id=chat_id,
                text='Новое объявление!',
                reply_markup=reply_markup
            )


def get_field_value(obj: Model, field: str):
    attrs = field.split('__')
    attr_value = obj
    for attr in attrs:
        attr_value = getattr(attr_value, attr, None)
        if attr_value is None:
            return None
    return attr_value


def get_filled_fields(obj: Model, fields) -> dict:
    filled_fields = {}
    for field in fields:
        value = get_field_value(obj, field)
        if value is not None:
            filled_fields[field] = value
    return filled_fields


async def send_message_to_subscribers(instance: Realty, chat_id):
    bot_token = os.getenv('TELEGRAM_TOKEN')
    bot = Bot(token=bot_token)
    async for user in TelegramUser.objects.filter(is_subscribed=True):
        keyboard = [
            [
                InlineKeyboardButton(
                    f'{instance.title}',
                    callback_data=f'realty_{instance.pk}'
                )
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await bot.send_message(
            chat_id=chat_id,
            text='Новое объявление!',
            reply_markup=reply_markup
        )
