import os

from dotenv import load_dotenv
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from tg_bot.handlers import (
    contact_handler,
    delete_handler,
    echo_handler,
    favorites_handler,
    show_realty,
    start_handler,
)
from tg_bot.handlers.review_handler import button, receive_review
from tg_bot.handlers.search_handler import handlers
from tg_bot.handlers.search_handler.callbacks import (
    back_to_list_handler,
    cancel_handler,
    main_menu,
    page_navigation_handler,
    realty_callback_handler,
)

load_dotenv()

ASK_FOR_REVIEW = 1


class TGBot:
    def __init__(self):
        self.ptb_app = (
            Application.builder()
            .token(os.getenv("TELEGRAM_TOKEN"))
            .updater(None)
            .build()
        )
        self.ptb_app.add_handler(
            ConversationHandler(
                entry_points=[
                    CallbackQueryHandler(button, pattern=r"^review_")
                ],
                states={
                    ASK_FOR_REVIEW: [
                        MessageHandler(
                            filters.TEXT & ~filters.COMMAND, receive_review
                        )
                    ],
                },
                fallbacks=[
                    CallbackQueryHandler(cancel_handler, pattern=r"^cancel$")
                ],
            )
        )
        self.ptb_app.add_handler(handlers.search_handler)
        self.ptb_app.add_handler(CommandHandler("start", start_handler.start))
        self.ptb_app.add_handler(CommandHandler("stop", delete_handler.delete))
        self.ptb_app.add_handler(
            CommandHandler("contacts", contact_handler.contacts)
        )
        self.ptb_app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, echo_handler.echo)
        )
        self.ptb_app.add_handler(
            CallbackQueryHandler(
                back_to_list_handler, pattern=r"^back_to_list$"
            )
        )
        self.ptb_app.add_handler(
            CallbackQueryHandler(cancel_handler, pattern=r"^cancel$")
        )
        self.ptb_app.add_handler(
            CallbackQueryHandler(realty_callback_handler, pattern=r"^realty_")
        )
        self.ptb_app.add_handler(
            CallbackQueryHandler(page_navigation_handler, pattern=r"^page_")
        )
        self.ptb_app.add_handler(
            CallbackQueryHandler(show_realty, pattern=r"^realty_")
        )
        self.ptb_app.add_handler(
            CallbackQueryHandler(button, pattern=r"^review_")
        )
        self.ptb_app.add_handler(
            CallbackQueryHandler(button, pattern=r"^view_reviews_")
        )
        self.ptb_app.add_handler(
            CommandHandler("my_favorites", favorites_handler.get_favorites)
        )
        self.ptb_app.add_handler(
            CallbackQueryHandler(
                favorites_handler.add_to_favorites,
                pattern=r"^add_to_favorite_",
            )
        )
        self.ptb_app.add_handler(
            CallbackQueryHandler(
                favorites_handler.delete_favorite, pattern=r"^delete_favorite_"
            )
        )
        self.ptb_app.add_handler(
            CallbackQueryHandler(main_menu, pattern="main_menu")
        )


tgbot = TGBot()
