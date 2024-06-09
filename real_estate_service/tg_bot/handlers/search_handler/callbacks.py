from datetime import datetime, timedelta

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes

from object.models import (
    Realty,
    Category,
    Condition,
    BuldingType
)
from .constants import MAIN_MENU, CHOOSE, TYPING, SAVE_CHOOSE, MAIN_FIELDS, OTHER_FIELDS
from .utils import edit_or_send, filter_args
from .keyboards import (
    city_keyboard, all_obj_keyboard,
    main_keyboard, other_keyboard
)
from .keyboards import (
    OTHER_CITY_KEYBOARD, AREA_KEYBOARD,
    PRICE_KEYBOARD, PUBLISH_DATE_KEYBOARD
)
from .texts import user_data_as_text


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Основное меню"""
    if 'location__city' not in context.user_data:
        return await location__city(update, context)
    reply_markup = InlineKeyboardMarkup(main_keyboard())
    main_text = user_data_as_text(context)
    await edit_or_send(update, context, main_text, reply_markup)
    return CHOOSE


async def location__city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Меню выбора города"""
    reply_markup = InlineKeyboardMarkup(await city_keyboard())
    context.user_data['choose'] = 'location__city'
    if 'location__city' in context.user_data:
        city_text = city_text = f'Выбранный ранее город: {context.user_data["location__city"]}'
    else:
        city_text = "Выбери город!"
    await edit_or_send(update, context, city_text, reply_markup)
    return SAVE_CHOOSE


async def other_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Меню выбора города, если его нет в списке основных городов. """
    query = update.callback_query
    await query.answer()
    reply_markup = InlineKeyboardMarkup(OTHER_CITY_KEYBOARD)
    if 'location__city' in context.user_data:
        text = f'Выбранный ранее город:{context.user_data["location__city"]}'
    else:
        text = "Выбери город!"
    await query.edit_message_text(text=text, reply_markup=reply_markup)
    return SAVE_CHOOSE


async def area(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Выбор диапазона площади"""
    query = update.callback_query
    await query.answer()
    markup = InlineKeyboardMarkup(AREA_KEYBOARD)
    context.user_data['choose'] = 'area'
    await query.edit_message_text(text='Выбери площадь', reply_markup=markup)
    return SAVE_CHOOSE


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Меню выбора диапазона цены."""
    query = update.callback_query
    await query.answer()
    markup = InlineKeyboardMarkup(PRICE_KEYBOARD)
    context.user_data['choose'] = 'price'
    await query.edit_message_text(text="Выбери цену", reply_markup=markup)
    return SAVE_CHOOSE


async def category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Меню выбора категории"""
    query = update.callback_query
    await query.answer()
    reply_markup = InlineKeyboardMarkup(await all_obj_keyboard(Category))
    context.user_data['choose'] = 'category'
    if 'category' in context.user_data:
        text = f'Выбранная ранее категория:{context.user_data["category"]}'
    else:
        text = "Выбери категорию!"
    await query.edit_message_text(text=text, reply_markup=reply_markup)
    return SAVE_CHOOSE


async def refresh_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Удалить все данные, кроме города"""
    query = update.callback_query
    await query.answer()
    for field in MAIN_FIELDS:
        if field in context.user_data and field != 'location__city':
            del context.user_data[field]
    return await main_menu(update, context)


async def represent_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать результаты поиска"""
    text = 'Here is your data:'
    realtys = []
    async for realty in Realty.objects.filter(**filter_args(context)):
        realtys.append(realty.title)
    if realtys:
        text = user_data_as_text(context)
        for realty in realtys:
            text += f'\n{realty}'
    else:
        text = 'Ничего подходящего=('
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton('Посмотрел', callback_data='Посмотрел')],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=text,  reply_markup=markup)
    return MAIN_MENU


async def other_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Дополнительное меню параметров поиска"""
    reply_markup = InlineKeyboardMarkup(other_keyboard())
    text = user_data_as_text(context)
    if not context.user_data.get('text_input'):
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            text=text,
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            text=text,
            reply_markup=reply_markup
        )
        del context.user_data['text_input']

    return CHOOSE


async def publish_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Меню выбора периода даты публикации"""
    markup = InlineKeyboardMarkup(PUBLISH_DATE_KEYBOARD)
    context.user_data['choose'] = 'publish_date'
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text='Выбери период публикации', reply_markup=markup)
    return SAVE_CHOOSE


async def condition(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Меню выбора состояния помещения"""
    query = update.callback_query
    await query.answer()
    reply_markup = InlineKeyboardMarkup(await all_obj_keyboard(Condition))
    context.user_data['choose'] = 'condition'
    if 'condition' in context.user_data:
        text = f'Выбранное ранее состояние помещений:{context.user_data["condition"]}'
    else:
        text = "Какое состояние помещений вас устроит?"
    await query.edit_message_text(text=text, reply_markup=reply_markup)
    return SAVE_CHOOSE


async def building_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Меню выбора типа здания"""
    query = update.callback_query
    await query.answer()
    reply_markup = InlineKeyboardMarkup(await all_obj_keyboard(BuldingType))
    context.user_data['choose'] = 'building_type'
    if 'building_type' in context.user_data:
        text = f'Выбранный ранее тип здания:{context.user_data["building_type"]}'
    else:
        text = "Ваберите тип здания, в которм нужны помещения."
    await query.edit_message_text(text=text, reply_markup=reply_markup)
    return SAVE_CHOOSE


async def text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt user to input data for selected feature."""
    context.user_data['choose'] = update.callback_query.data
    text = "Okay, tell me."

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text)
    return TYPING


async def save_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save text for feature and return to other menu."""
    user_data = context.user_data
    user_data[user_data['choose']] = update.message.text
    context.user_data['text_input'] = True
    return await other_menu(update, context)


async def save_choose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    query = update.callback_query
    await query.answer()
    user_data[user_data['choose']] = query.data
    if user_data['choose'] in MAIN_FIELDS:
        return await main_menu(update, context)
    return await other_menu(update, context)


async def refresh_other(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Удалить все данные, вводимые во вспмогатльном меню"""
    query = update.callback_query
    await query.answer()
    for field in OTHER_FIELDS:
        if field in context.user_data:
            del context.user_data[field]
    return await other_menu(update, context)
