from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from .base_utils import (get_all_realty, get_favorite_exists,
                         get_or_create_telegram_user, get_realty_by_id,
                         get_user_by_id)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tg_id = update.message.from_user.id
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    username = update.message.from_user.username

    tg_user, created = await get_or_create_telegram_user(
        tg_id, first_name, last_name, username
    )
    if created:
        text = f"Привет {username}"
        await update.message.reply_html(text=text)

    realty_list = await get_all_realty()
    buttons = [
        [InlineKeyboardButton(realty.title, callback_data=f"realty_{realty.id}")]
        for realty in realty_list
    ]

    reply_markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(
        "Список объектов недвижимости:", reply_markup=reply_markup
    )
