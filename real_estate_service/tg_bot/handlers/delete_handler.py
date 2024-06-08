from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import ContextTypes

from user.models import TelegramUser


async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for start command"""
    user_id = update.effective_user.id
    await sync_to_async(TelegramUser.objects.filter(tg_id=user_id).delete)()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Ваш аккаунт был успешно удален. Все ваши данные были стерты из нашей базы данных."
    )
