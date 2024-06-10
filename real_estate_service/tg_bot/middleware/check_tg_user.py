from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import ContextTypes
from django.shortcuts import get_object_or_404

from user.models import TelegramUser

@sync_to_async
def is_user_blocked(user_id):
    try:
        telegram_user = TelegramUser.objects.get(tg_id=user_id)
        return telegram_user.is_blocked
    except TelegramUser.DoesNotExist:
        return False
