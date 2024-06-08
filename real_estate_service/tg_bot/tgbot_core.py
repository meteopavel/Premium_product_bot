import os

from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from tg_bot.handlers import start_handler, echo_handler, delete_handler
from tg_bot.handlers.search_handler import handlers

load_dotenv()


class TGBot:
    def __init__(self):
        self.ptb_app = (
            Application.builder()
            .token(os.getenv('TELEGRAM_TOKEN'))
            .updater(None)
            .build()
        )
        self.ptb_app.add_handler(CommandHandler("start", start_handler.start))
        self.ptb_app.add_handler(CommandHandler("stop", delete_handler.delete))
        # self.ptb_app.add_handler(
        #    MessageHandler(filters.TEXT & ~filters.COMMAND, echo_handler.echo)
        # )
        self.ptb_app.add_handler(handlers.search_handler)


tgbot = TGBot()
