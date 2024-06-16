#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from typing import Dict
import re
from datetime import datetime, timedelta

from telegram import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler
)
from object.models import (
    City,
    Realty,
    Category,
    Condition,
    BuldingType
)
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

MAIN_MENU, SAVE_DATA, CHOOSE, CHOOSE_OTHER, TYPING, SAVE_MAIN_CHOOSE, SAVE_OTHER_CHOOSE = range(
    7)

search_fields = ['city', 'area', 'price', 'category',
                 'publish_date', 'condition', 'building_type', 'text']
foregin_fields = ['city', 'category', 'condition', 'building_type',]
integer_fields = ['area', 'price']
datetive_fields = ['publish_date']
text_fields = ['text']


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send message on `/start`."""
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    keyboard = [
        [
            InlineKeyboardButton("ПОИСК!", callback_data="ПОИСК!"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Start handler, Choose your desteny!", reply_markup=reply_markup)
    if 'city' in context.user_data:
        return MAIN_MENU
    return CHOOSE


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Основное меню"""
    keyboard = [
        [InlineKeyboardButton('Категория', callback_data='category')],
        [InlineKeyboardButton('Площадь', callback_data='area')],
        [InlineKeyboardButton('Цена', callback_data='price')],
        [
            InlineKeyboardButton('Прочее', callback_data='other'),
            InlineKeyboardButton('Изменить город', callback_data='city')
        ],
        [
            InlineKeyboardButton('Показать результат',
                                 callback_data='represent_results'),
            InlineKeyboardButton('Очистить фаильтры',
                                 callback_data='refresh_all'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=f'Ваш город: {context.user_data["city"]}',
        reply_markup=reply_markup
    )
    return CHOOSE


async def city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Меню выбора города"""
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
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.user_data['choose'] = 'city'
    if 'city' in context.user_data:
        text = f'Выбранный ранее город:{context.user_data["city"]}'
    else:
        text = "Выбери город!"
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=text, reply_markup=reply_markup)
    return SAVE_MAIN_CHOOSE


async def other_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Меню выбора города, если его нет в списке основных городов. """
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton(
            'Какойто город', callback_data='выбрал-Какойто город')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if 'city' in context.user_data:
        text = f'Выбранный ранее город:{context.user_data["city"]}'
    else:
        text = "Выбери город!"
    await query.edit_message_text(text=text, reply_markup=reply_markup)
    return SAVE_MAIN_CHOOSE


async def area(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Выбор диапазона площади"""
    query = update.callback_query
    await query.answer()
    keyboard = [[InlineKeyboardButton('1-150', callback_data='1-150')],
                [InlineKeyboardButton(
                    '150-1000', callback_data='150-1000')],
                [InlineKeyboardButton('1000-100000', callback_data='1000-100000')]]
    markup = InlineKeyboardMarkup(keyboard)
    context.user_data['choose'] = 'area'
    await query.edit_message_text(text=f"Выбери площадь", reply_markup=markup)
    return SAVE_MAIN_CHOOSE


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Меню выбора диапазона цены."""
    query = update.callback_query
    await query.answer()
    keyboard = [[InlineKeyboardButton('1-150', callback_data='1-150')],
                [InlineKeyboardButton(
                    '150-1000', callback_data='150-1000')],
                [InlineKeyboardButton('1000-100000', callback_data='1000-100000')]]
    markup = InlineKeyboardMarkup(keyboard)
    context.user_data['choose'] = 'price'
    await query.edit_message_text(text=f"Выбери цену", reply_markup=markup)
    return SAVE_MAIN_CHOOSE


async def category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Меню выбора категории"""
    query = update.callback_query
    await query.answer()
    keyboard = []
    async for category in Category.objects.all().values_list('name', flat=True):
        keyboard.append(
            [
                InlineKeyboardButton(category, callback_data=category)
            ]
        )
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.user_data['choose'] = 'category'
    if 'category' in context.user_data:
        text = f'Выбранная ранее категория:{context.user_data["category"]}'
    else:
        text = "Выбери категорию!"
    await query.edit_message_text(text=text, reply_markup=reply_markup)
    return SAVE_MAIN_CHOOSE


async def refresh_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Удалить все данные, кроме города"""
    pass

search_fields: list[str] = ['city', 'area', 'price', 'category',
                            'publish_date', 'condition', 'building_type', 'text']
foregin_fields = ['city', 'category', 'condition', 'building_type',]
integer_fields = ['area', 'price']
datetime_field = 'publish_date'
text_fields = ['text']


async def represent_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать результаты поиска"""
    text = 'Here is your data:'
    filter_args = {}
    for field in foregin_fields:
        if field in context.user_data:
            query = field + '__name'
            data = context.user_data[field]
            filter_args[query] = data
    for field in integer_fields:
        if field in context.user_data:
            query = field + '__lte'
            minimum = context.user_data[field].split('-')[0]
            maximum = context.user_data[field].split('-')[1]
            filter_args[query] = maximum
            query = field + '__gt'
            filter_args[query] = minimum
    if datetime_field in context.user_data:
        query = datetime_field + '__range'
        days_to_subtract = int(context.user_data[datetime_field])
        end_date = datetime.today()
        start_date = end_date - timedelta(days=days_to_subtract)
        filter_args[query] = (start_date, end_date)
    realtys = []
    async for realty in Realty.objects.filter(**filter_args):
        realtys.append(realty.title)
    if realtys:
        text = 'Результат вот'
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


def filter_main_menu(data):
    """Сравнивает данные с регулянрным выражением.
    Callable для pattern CallbackQueryHandler"""
    input_string = str(data)
    regex_pattern = r'^(other_city|refresh_all)$'
    return not bool(re.match(regex_pattern, input_string))


async def save_main_choose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    query = update.callback_query
    await query.answer()
    user_data[user_data['choose']] = query.data
    return await main_menu(update, context)


async def other_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Дополнительное меню параметров поиска"""
    keyboard = [
        [InlineKeyboardButton(
            'Дата обновления', callback_data='publish_date')],
        [InlineKeyboardButton('Состояние помещения',
                              callback_data='condition')],
        [InlineKeyboardButton('Тип здания', callback_data='building_type')],
        [InlineKeyboardButton('Поиск в тексте обьявления',
                              callback_data='text')],
        [
            InlineKeyboardButton(
                'Сбросить', callback_data='refresh_other'),
            InlineKeyboardButton('Вернуться в меню',
                                 callback_data='return_to_main'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = f'Ваш город: {context.user_data["city"]}'
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

    return CHOOSE_OTHER


async def publish_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Меню выбора периода даты публикации"""
    keyboard = [[InlineKeyboardButton('Сегодняшние', callback_data='1')],
                [InlineKeyboardButton('За неделю', callback_data='7')],
                [InlineKeyboardButton('За месяц', callback_data='31')],
                [InlineKeyboardButton('Полгода', callback_data='184')]]
    markup = InlineKeyboardMarkup(keyboard)
    context.user_data['choose'] = 'publish_date'
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f"Выбери период публикации", reply_markup=markup)
    return SAVE_OTHER_CHOOSE


async def condition(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Меню выбора состояния помещения"""
    query = update.callback_query
    await query.answer()
    keyboard = []
    async for condition in Condition.objects.all().values_list('name', flat=True):
        keyboard.append(
            [
                InlineKeyboardButton(condition, callback_data=condition)
            ]
        )
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.user_data['choose'] = 'condition'
    if 'condition' in context.user_data:
        text = f'Выбранное ранее состояние помещений:{context.user_data["condition"]}'
    else:
        text = "Какое состояние помещений вас устроит?"
    await query.edit_message_text(text=text, reply_markup=reply_markup)
    return SAVE_OTHER_CHOOSE


async def building_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Меню выбора типа здания"""
    query = update.callback_query
    await query.answer()
    keyboard = []
    async for building_type in BuldingType.objects.all().values_list('name', flat=True):
        keyboard.append(
            [
                InlineKeyboardButton(
                    building_type, callback_data=building_type)
            ]
        )
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.user_data['choose'] = 'building_type'
    if 'building_type' in context.user_data:
        text = f'Выбранное ранее состояние помещений:{context.user_data["building_type"]}'
    else:
        text = "Ваберите тип здания, в которм нужны помещения."
    await query.edit_message_text(text=text, reply_markup=reply_markup)
    return SAVE_OTHER_CHOOSE


async def text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Prompt user to input data for selected feature."""
    context.user_data['choose'] = update.callback_query.data
    text = "Okay, tell me."

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text)
    return TYPING


async def save_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Save text for feature and return to other menu."""
    user_data = context.user_data
    user_data[user_data['choose']] = update.message.text
    context.user_data['text_input'] = True
    return await other_menu(update, context)


async def save_other_choose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    query = update.callback_query
    await query.answer()
    user_data[user_data['choose']] = query.data
    return await other_menu(update, context)


async def refresh_other(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Удалить все данные, вводимые во вспмогатльном меню"""
    pass


def main(token) -> None:
    """Run the bot."""
    application = Application.builder().token(token).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSE: [
                CallbackQueryHandler(city, pattern='^(city|ПОИСК!)$'),
                CallbackQueryHandler(area, pattern='^area$'),
                CallbackQueryHandler(price, pattern='^price$'),
                CallbackQueryHandler(category, pattern='^category$'),
                CallbackQueryHandler(
                    represent_results, pattern='^represent_results$'),
                CallbackQueryHandler(other_menu, pattern='^other$'),
                CallbackQueryHandler(refresh_all, pattern='^refresh_all$')
            ],
            SAVE_MAIN_CHOOSE: [
                CallbackQueryHandler(
                    save_main_choose, pattern=filter_main_menu),
                CallbackQueryHandler(other_city, pattern='^other_city$'),
            ],
            MAIN_MENU: [
                CallbackQueryHandler(
                    main_menu,
                    pattern=filter_main_menu
                ),
            ],
            SAVE_OTHER_CHOOSE: [
                CallbackQueryHandler(
                    save_other_choose),
            ],
            CHOOSE_OTHER: [
                CallbackQueryHandler(condition, pattern='^condition$'),
                CallbackQueryHandler(building_type, pattern='^building_type$'),
                CallbackQueryHandler(text, pattern='^text$'),
                CallbackQueryHandler(publish_date, pattern='^publish_date$'),
                CallbackQueryHandler(refresh_other, pattern='^refresh_other$'),
                CallbackQueryHandler(main_menu, pattern='^return_to_main$'),
            ],
            TYPING: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, save_text)
            ]

        },
        fallbacks=[MessageHandler(filters.Regex(
            "^Done$"), start)],
    )

    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
