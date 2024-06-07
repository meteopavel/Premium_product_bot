from asgiref.sync import sync_to_async
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from user.models import TelegramUser
from object.models import Realty
import math


@sync_to_async
def get_realty_by_id(realty_id):
    return Realty.objects.get(id=realty_id)

@sync_to_async
def get_or_create_telegram_user(tg_id, first_name, last_name, username):
    return TelegramUser.objects.get_or_create(
        tg_id=tg_id,
        first_name=first_name,
        last_name=last_name,
        username=username,
    )

@sync_to_async
def get_all_realty():
    return list(Realty.objects.all())

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tg_id = update.message.from_user.id
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    username = update.message.from_user.username

    tg_user, created = await get_or_create_telegram_user(tg_id, first_name, last_name, username)
    if created:
        text = f'Привет {username}'
        await update.message.reply_html(text=text)

    realty_list = await get_all_realty()
    buttons = [
        [InlineKeyboardButton(realty.title, callback_data=f"realty_{realty.id}")]
        for realty in realty_list
    ]

    reply_markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text("Список объектов недвижимости:", reply_markup=reply_markup)

async def realty_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    realty_id = query.data.split("_")[1]

    realty = await get_realty_by_id(realty_id)

    buttons = [
        [InlineKeyboardButton("Оставить отзыв", callback_data=f"review_{realty_id}")],
        [InlineKeyboardButton("Посмотреть отзывы", callback_data=f"view_reviews_{realty_id}")]
    ]

    reply_markup = InlineKeyboardMarkup(buttons)
    await query.message.reply_text(f"Объект недвижимости: {realty.title}", reply_markup=reply_markup)
