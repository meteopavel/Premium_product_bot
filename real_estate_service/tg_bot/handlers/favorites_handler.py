from asgiref.sync import sync_to_async
from django.db.utils import IntegrityError
from favorites.models import Favorite
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

from .base_utils import (
    create_favorites,
    get_favorites_by_user,
    get_realty_by_id,
    get_user_by_id,
)
from .search_handler.constants import LOGO_URL_RELATIVE


@sync_to_async
def get_buttons(all_favorites):
    """Handler for getting all favorite button"""
    buttons = []
    for favorite_realty in all_favorites:
        title = favorite_realty.realty.title
        if not favorite_realty.realty.is_active:
            title += " - удалено админом"
        buttons.append(
            [
                InlineKeyboardButton(
                    title,
                    callback_data=f"realty_{favorite_realty.realty.id}",
                )
            ]
        )
    return buttons


async def get_favorites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler to get your favorites"""
    user = await get_user_by_id(update.effective_user.id)
    if not user.is_blocked:
        all_favorites = await get_favorites_by_user(user)
        buttons = await get_buttons(all_favorites)
        if buttons:
            response_list = InlineKeyboardMarkup(buttons)
            await update.message.reply_photo(
                photo=LOGO_URL_RELATIVE,
                caption="Ваше избранное:",
                reply_markup=response_list,
            )
        else:
            await update.message.reply_text("Тут пока ничего нет")
    else:
        await update.message.reply_text(
            "⚠️ <b>Вы были заблокированы. Обратитесь к администратору!</b>",
            parse_mode="HTML",
        )
    return ConversationHandler.END


async def add_to_favorites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for adding realty to favorites"""
    try:
        query = update.callback_query
        await query.answer()
        user = await get_user_by_id(update.effective_user.id)
        if not user.is_blocked:
            realty = await get_realty_by_id(query.data.split("_")[3])
            await create_favorites(user=user, realty=realty)
            message_text = "Объект недвижимости добавлен в избранное 🌟"
            await query.message.reply_text(message_text)
        else:
            message_text = (
                "⚠️ Вы были заблокированы. Обратитесь к администратору!"
            )
            await query.message.reply_text(message_text)
    except IntegrityError:
        message_text = "Объект недвижимости уже в избранном 🌟"
        await query.message.reply_text(message_text)


async def delete_favorite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for deleting favorites"""
    try:
        query = update.callback_query
        await query.answer()
        user = await get_user_by_id(update.effective_user.id)
        if not user.is_blocked:
            realty = await get_realty_by_id(query.data.split("_")[2])
            await sync_to_async(
                Favorite.objects.filter(user=user, realty=realty).delete
            )()
            message_text = "Объект недвижимости удален из избранного 🌟"
            await query.message.reply_text(message_text)
        else:
            message_text = (
                "⚠️ Вы были заблокированы. Обратитесь к администратору!"
            )
            await query.message.reply_text(message_text)
    except Exception:
        message_text = "Упс, что-то пошло не так!"
        await query.message.reply_text(message_text)
