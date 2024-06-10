import os

from dotenv import load_dotenv
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          MessageHandler, filters)

from tg_bot.handlers import (delete_handler, echo_handler, favorites_handler,
                             review_handler, start_handler)
from tg_bot.handlers.search_handler import handlers
from tg_bot.handlers.search_handler.callbacks import represent_results

load_dotenv()


class TGBot:
    def __init__(self):
        self.ptb_app = (
            Application.builder()
            .token(os.getenv("TELEGRAM_TOKEN"))
            .updater(None)
            .build()
        )
        self.ptb_app.add_handler(CommandHandler("start", start_handler.start))
        self.ptb_app.add_handler(CommandHandler("stop", delete_handler.delete))
        # self.ptb_app.add_handler(
        #    MessageHandler(filters.TEXT & ~filters.COMMAND, echo_handler.echo)
        # )
        self.ptb_app.add_handler(handlers.search_handler)
        self.ptb_app.add_handler(CallbackQueryHandler(represent_results, pattern=r"^realty_"))
        self.ptb_app.add_handler(CallbackQueryHandler(review_handler.button, pattern=r"^review_"))
        self.ptb_app.add_handler(CallbackQueryHandler(review_handler.button, pattern=r"^view_reviews_"))
        self.ptb_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, review_handler.receive_review))
        self.ptb_app.add_handler(CommandHandler("my_favorites", favorites_handler.get_favorites))
        self.ptb_app.add_handler(CallbackQueryHandler(favorites_handler.add_to_favorites, pattern=r"^add_to_favorite_"))
        self.ptb_app.add_handler(CallbackQueryHandler(favorites_handler.delete_favorite, pattern=r"^delete_favorite_"))
        self.ptb_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_handler.echo))


tgbot = TGBot()