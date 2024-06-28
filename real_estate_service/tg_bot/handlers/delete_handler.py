from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import ContextTypes

from user.models import TelegramUser
from .base_utils import arhive_user


async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for stop command"""
    user_id = update.effective_user.id
    user = await TelegramUser.objects.filter(tg_id=user_id).afirst()
    if not user:
        return
    await arhive_user(user_id)
    await sync_to_async(user.delete)()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=("Ваш аккаунт был успешно удален."
              "Параметры поиска и избранного будут храниться 30 дней")
    )
