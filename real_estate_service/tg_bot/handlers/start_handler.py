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


async def realty_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    realty_id = query.data.split("_")[1]

    realty = await get_realty_by_id(realty_id)
    user = await get_user_by_id(update.effective_user.id)
    if await get_favorite_exists(user, realty):
        button = [
            InlineKeyboardButton(
                "Удалить из избранного", callback_data=f"delete_favorite_{realty_id}"
            )
        ]
    else:
        button = [
            InlineKeyboardButton(
                "Добавить в избранное", callback_data=f"add_to_favorite_{realty_id}"
            )
        ]
    buttons = [
        [InlineKeyboardButton("Оставить отзыв", callback_data=f"review_{realty_id}")],
        [InlineKeyboardButton("Посмотреть отзывы", callback_data=f"view_reviews_{realty_id}")],
        button,
    ]

    reply_markup = InlineKeyboardMarkup(buttons)
    await query.message.reply_text(
        f"Объект недвижимости: {realty.title}", reply_markup=reply_markup
    )
