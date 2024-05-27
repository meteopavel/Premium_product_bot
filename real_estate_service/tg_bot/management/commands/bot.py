import os

from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from telegram import Bot, Update
from telegram.ext import (
    Updater, MessageHandler, Filters, CallbackContext
)

from user.models import User

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


def do_echo(update: Update, context: CallbackContext):
    telegram_id = update.message.from_user.id
    username = update.message.from_user.username
    firstname = update.message.from_user.first_name
    lastname = update.message.from_user.last_name
    chat_id = update.message.chat_id
    text = update.message.text

    User.objects.get_or_create(
        telegram_id=telegram_id,
        username=username,
        telegram_username=username,
        first_name=firstname,
        telegram_firstname=firstname,
        last_name=lastname,
        telegram_lastname=lastname,
    )

    reply_text = (f'Ваш id = {telegram_id}\n'
                  f'ID чата = {chat_id}\n'
                  f'Текст = {text}')
    update.message.reply_text(
        text=reply_text,
    )


class Command(BaseCommand):
    help = 'Команда для запуска бота.'

    def handle(self, *args, **kwargs):
        bot = Bot(token=TELEGRAM_TOKEN)
        print(bot.get_me())

        updater = Updater(bot=bot, use_context=True)

        message_handler = MessageHandler(Filters.text, do_echo)
        updater.dispatcher.add_handler(message_handler)

        updater.start_polling()
        updater.idle()
