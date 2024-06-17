from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Update,
)
from telegram.ext import ContextTypes, ConversationHandler

from object.models import Realty
from tg_bot.handlers.base_utils import get_favorite_exists, get_user_by_id


async def show_realty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    pk: int = int(query.data.split("_")[-1])

    realty = await Realty.objects.select_related(
        "category", "location__city", "contact", "condition", "building_type"
    ).aget(pk=pk)

    user = await get_user_by_id(update.effective_user.id)
    category = realty.category
    location = realty.location.city if realty.location else None
    contact = realty.contact
    condition = realty.condition
    building_type = realty.building_type

    favorite_exists = await get_favorite_exists(user, realty)

    if favorite_exists:
        favorite_button = InlineKeyboardButton(
            "Удалить из избранного", callback_data=f"delete_favorite_{pk}"
        )
    else:
        favorite_button = InlineKeyboardButton(
            "Добавить в избранное", callback_data=f"add_to_favorite_{pk}"
        )

    buttons = [
        [InlineKeyboardButton("Оставить отзыв", callback_data=f"review_{pk}")],
        [
            InlineKeyboardButton(
                "Посмотреть отзывы", callback_data=f"view_reviews_{pk}"
            )
        ],
        [favorite_button],
        [InlineKeyboardButton("Назад", callback_data="back_to_list")],
    ]

    condition_text = "Состояние помещения:"
    reply_markup = InlineKeyboardMarkup(buttons)
    text = (
        f"Объект недвижимости: {realty.title}\n"
        f"Площадь: {realty.area} кв.м\n"
        f"Цена: {realty.price if realty.price else 'Не указано'} руб.\n"
        f"Категория: {category.name if category else 'Не указана'}\n"
        f"Локация: {location.name if location else 'Не указана'}\n"
        f"Контакт: {contact.name if contact else 'Не указан'}\n"
        f"{condition_text} {condition.name if condition else 'Не указано'}\n"
        f"Тип здания: {building_type.name if building_type else 'Не указан'}\n"
        f"Описание: {realty.text if realty.text else 'Не указано'}"
    )
    await query.edit_message_media(
        media=InputMediaPhoto(media=realty.image, caption=text),
        reply_markup=reply_markup,
    )
    return ConversationHandler.END
