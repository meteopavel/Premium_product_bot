from asgiref.sync import sync_to_async
from favorites.models import Favorite
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from .base_utils import (create_favorites, get_favorites_by_user,
                         get_realty_by_id, get_user_by_id)


@sync_to_async
def get_buttons(all_favorites):
    return [
        [
            InlineKeyboardButton(
                favorite_realty.realty.title,
                callback_data=f"realty_{favorite_realty.realty.id}",
            )
        ]
        for favorite_realty in all_favorites
    ]


async def get_favorites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler to get your favorites"""
    user = await get_user_by_id(update.effective_user.id)
    if not user.is_blocked:
        all_favorites = await get_favorites_by_user(user)
        buttons = await get_buttons(all_favorites)
        if buttons:
            response_list = InlineKeyboardMarkup(buttons)
            await update.message.reply_text(
                "Ваше избранное:", reply_markup=response_list
            )
        else:
            await update.message.reply_text("Тут пока ничего нет")
    else:
        await update.message.reply_text(
            "⚠️ <b>Вы были заблокированы. Обратитесь к администратору!</b>",
            parse_mode="HTML",
        )


async def add_to_favorites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = await get_user_by_id(update.effective_user.id)
    if not user.is_blocked:
        realty = await get_realty_by_id(query.data.split("_")[3])
        await create_favorites(user=user, realty=realty)
        message_text = "Объект недвижимости добавлен в избранное 🌟"
        await query.message.reply_text(message_text)
    else:
        message_text = "⚠️ Вы были заблокированы. Обратитесь к администратору!"
        await query.message.reply_text(message_text)


async def delete_favorite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = await get_user_by_id(update.effective_user.id)
    if not user.is_blocked:
        realty = await get_realty_by_id(query.data.split("_")[2])
        await sync_to_async(Favorite.objects.filter(user=user, realty=realty).delete)()
        message_text = "Объект недвижимости удален из избранного 🌟"
        await query.message.reply_text(message_text)
    else:
        message_text = "⚠️ Вы были заблокированы. Обратитесь к администратору!"
        await query.message.reply_text(message_text)
