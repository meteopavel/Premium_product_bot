import json
from datetime import datetime, timedelta

from telegram import Update, InputMediaPhoto
from telegram.ext import ContextTypes
from asgiref.sync import sync_to_async

from user.models import TelegramUser
from .constants import LOGO_URL_ABSOLUTE, LOGO_URL_RELATIVE


def dict_to_string(dictionary):
    """
    Преобразует словарь в строку формата JSON.

    :param dictionary: Словарь для преобразования
    :return: Строка формата JSON
    """
    try:
        return json.dumps(dictionary, ensure_ascii=False,)
    except (TypeError, ValueError) as e:
        print(f'Ошибка при преобразовании словаря в строку: {e}')
        return None


def string_to_dict(string):
    """
    Преобразует строку формата JSON обратно в словарь.

    :param string: Строка формата JSON
    :return: Словарь
    """
    try:
        return json.loads(string)
    except (TypeError, ValueError) as e:
        print(f'Ошибка при преобразовании строки в словарь: {e}')
        return None


async def edit_or_send(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        text,
        reply_markup=None
) -> None:
    """Проверит запрос. Если он есть - обновит сообщение.
    Если нет то просто отправит"""
    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_media(
            media=InputMediaPhoto(
                media=LOGO_URL_ABSOLUTE,
                caption=text
            ),
            reply_markup=reply_markup
        )
    else:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=LOGO_URL_RELATIVE,
            caption=text,
            reply_markup=reply_markup
        )
# Вспомогательные штучки
search_fields: list[str] = [
    'location__city', 'area', 'price', 'category',
    'publish_date', 'condition', 'building_type', 'text'
]
foregin_fields = ['location__city', 'category', 'condition', 'building_type',]
integer_fields = ['area', 'price']
datetime_field = 'publish_date'
text_field = 'text'


def filter_args(
        user_data
) -> dict:
    """Формирует словарь аргументов для запроса к БД
    через ORM."""
    args = {}
    for field in foregin_fields:
        if field in user_data:
            query = field
            str_data = user_data[field]
            data = string_to_dict(str_data)
            args[query] = int(data)
    for field in integer_fields:
        if field in user_data:
            query = field + '__lte'
            minimum = user_data[field].split('-')[0]
            maximum = user_data[field].split('-')[1]
            args[query] = maximum
            query = field + '__gt'
            args[query] = minimum
    if datetime_field in user_data:
        query = datetime_field + '__range'
        days_to_subtract = int(user_data[datetime_field])
        end_date = datetime.today()
        start_date = end_date - timedelta(days=days_to_subtract)
        args[query] = (start_date, end_date)
    if text_field in user_data:
        query = text_field + '__icontains'
        data = user_data[field]
        args[query] = data
    return args


async def save_search_parameters(
        update: Update, context: ContextTypes.DEFAULT_TYPE
):
    user = await TelegramUser.objects.filter(
        tg_id=update.effective_chat.id
    ).afirst()
    if not user:
        return False
    search_parameters = {}
    for field in search_fields:
        if field in context.user_data:
            search_parameters[field] = context.user_data[field]
    search_parameters = dict_to_string(search_parameters)
    user.search_parameters = search_parameters
    await sync_to_async(user.save)()
    return True


async def save_is_subscribed(tg_id: int, is_subscribed: bool):
    user = await TelegramUser.objects.filter(
        tg_id=tg_id
    ).afirst()
    user.is_subscribed = is_subscribed
    await sync_to_async(user.save)()
    return


async def unpack_search_parameters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await TelegramUser.objects.filter(
        tg_id=update.effective_chat.id
    ).afirst()
    if not user:
        return False
    search_params = string_to_dict(user.search_parameters)
    if search_params:
        for param in search_params:
            context.user_data[param] = search_params[param]
    return True


async def insert_media_with_caption(query, media, text, markup):
    await query.edit_message_media(
        media=InputMediaPhoto(media=media, caption=text),
        reply_markup=markup
    )