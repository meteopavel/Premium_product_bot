from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import ContextTypes

from user.models import TelegramUser


@sync_to_async
def get_or_create_telegram_user(tg_id, first_name, last_name, username):
    return TelegramUser.objects.get_or_create(
        tg_id=tg_id,
        first_name=first_name,
        last_name=last_name,
        username=username,
    )


async def start(update: Update,
                context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for start command"""
    tg_id = update.message.from_user.id
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    username = update.message.from_user.username

    tg_user, created = await get_or_create_telegram_user(tg_id, first_name, last_name, username)
    if created:
        text = f'{username}, welcome to realty bot'
        await update.message.reply_html(text=text)
