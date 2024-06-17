from telegram import Update
from telegram.ext import ContextTypes

from .base_utils import get_or_create_telegram_user


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for start button"""
    tg_id = update.message.from_user.id
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    username = update.message.from_user.username

    tg_user, created = await get_or_create_telegram_user(
        tg_id, first_name, last_name, username
    )
    text = ""
    if created:
        text = f"Привет {username}\n"
    else:
        text = f"С возвращением, {username}\n"

    info_text = (
        "Введите команду:\n/search - чтобы начать поиск"
        " недвижимости;\n/my_favorites - чтобы посмотреть все ваши"
        " избранные;\n/contacts - наши контакты;\n/stop -"
        " чтобы удалиться из бота;"
    )
    full_text = text + info_text
    await update.message.reply_html(text=full_text)
