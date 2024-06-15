from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from object.models import Realty
from tg_bot.handlers.search_handler.utils import save_search_parameters
from tg_bot.handlers.base_utils import get_realty_by_id, get_user_by_id, get_favorite_exists


async def show_realty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    pk: int = int(query.data.split('_')[-1])
    realty = await Realty.objects.filter(pk=pk).afirst()
    user = await get_user_by_id(update.effective_user.id)

    if await get_favorite_exists(user, realty):
        favorite_button = InlineKeyboardButton(
            "Удалить из избранного", callback_data=f"delete_favorite_{pk}"
        )
    else:
        favorite_button = InlineKeyboardButton(
            "Добавить в избранное", callback_data=f"add_to_favorite_{pk}"
        )

    buttons = [
        [InlineKeyboardButton("Оставить отзыв", callback_data=f"review_{pk}")],
        [InlineKeyboardButton("Посмотреть отзывы", callback_data=f"view_reviews_{pk}")],
        [favorite_button],
        [InlineKeyboardButton('Назад', callback_data=f'back_to_list')]
    ]

    reply_markup = InlineKeyboardMarkup(buttons)
    await query.edit_message_text(
        f"Объект недвижимости: {realty.title}", reply_markup=reply_markup
    )
    return ConversationHandler.END
