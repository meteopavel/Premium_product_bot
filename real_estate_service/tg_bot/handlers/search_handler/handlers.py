from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, MessageHandler, filters)

from .. import show_realty
from .callbacks import (area, building_type, cancel, category, city_typing,
                        condition, location__city, main_menu, other_citys_list,
                        other_menu, price, publish_date, refresh_all,
                        refresh_other, rep_button, rep_button2,
                        represent_results, save_choose, save_text, subscribe,
                        text)
from .constants import (CHOOSE, CITY_TYPING, MAIN_FIELDS, OTHER_FIELDS,
                        REPRESENT, REPRESENT_CITYS, SAVE_CHOOSE, TYPING)
from .filters import filter_main_menu, filter_rep_city

search_handler = ConversationHandler(
    entry_points=[CommandHandler("search", main_menu)],
    states={
        CHOOSE: [
            CallbackQueryHandler(
                globals()[field], pattern="^" + f"{field}" + "$"
            )
            for field in list(MAIN_FIELDS) + list(OTHER_FIELDS)
        ]
        + [
            CallbackQueryHandler(
                represent_results, pattern="^represent_results$"
            ),
            CallbackQueryHandler(other_menu, pattern="^other$"),
            CallbackQueryHandler(refresh_all, pattern="^refresh_all$"),
            CallbackQueryHandler(main_menu, pattern="^return_to_main$"),
            CallbackQueryHandler(refresh_other, pattern="^refresh_other$"),
            CallbackQueryHandler(subscribe, pattern="^subscribe_"),
        ],
        SAVE_CHOOSE: [
            CallbackQueryHandler(save_choose, pattern=filter_main_menu),
            CallbackQueryHandler(city_typing, pattern="^city_typing$"),
            CallbackQueryHandler(main_menu, pattern="^menu$"),
            CallbackQueryHandler(other_menu, pattern="^other_menu$"),
        ],
        TYPING: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_text)],
        CITY_TYPING: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, other_citys_list),
            CallbackQueryHandler(main_menu, pattern="^main_menu$"),
        ],
        REPRESENT: [
            CallbackQueryHandler(rep_button, pattern="^(page)"),
            CallbackQueryHandler(main_menu, pattern="^main_menu$"),
            CallbackQueryHandler(show_realty.show_realty, pattern="^realty_"),
        ],
        REPRESENT_CITYS: [
            CallbackQueryHandler(rep_button2, pattern="^(page|main_menu)"),
            CallbackQueryHandler(save_choose, pattern=filter_rep_city),
            CallbackQueryHandler(city_typing, pattern="^city_typing$"),
        ],
    },
    fallbacks=[
        CommandHandler("cancel", cancel),
        CommandHandler("start", cancel),
        CommandHandler("stop", cancel),
        CommandHandler("my_favorites", cancel),
        CallbackQueryHandler(cancel, pattern="^cancel$"),
        MessageHandler(filters.TEXT & ~filters.COMMAND, cancel),
    ],
)
