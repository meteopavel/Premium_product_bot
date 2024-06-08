from telegram.ext import (
    ConversationHandler,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters
)

from .callbacks import (
    main_menu, location__city, category, price,
    other_city, other_menu, area, publish_date,
    condition, represent_results, refresh_all, refresh_other,
    save_choose, condition, building_type, text,
    publish_date, save_text
)
from .constants import MAIN_MENU, CHOOSE, \
    TYPING, SAVE_CHOOSE, \
    MAIN_FIELDS, OTHER_FIELDS
from .filters import filter_chose
from tg_bot.handlers.start_handler import start

search_handler = ConversationHandler(
    entry_points=[CommandHandler('search', main_menu)],
    states={
        CHOOSE: [
            CallbackQueryHandler(
                globals()[field], pattern='^'+f'{field}'+'$'
            ) for field in list(MAIN_FIELDS) + list(OTHER_FIELDS)
        ] + [
            CallbackQueryHandler(
                represent_results, pattern='^represent_results$'),
            CallbackQueryHandler(other_menu, pattern='^other$'),
            CallbackQueryHandler(refresh_all, pattern='^refresh_all$'),
            CallbackQueryHandler(main_menu, pattern='^return_to_main$'),
            CallbackQueryHandler(refresh_other, pattern='^refresh_other$')
        ],
        SAVE_CHOOSE: [
            CallbackQueryHandler(
                save_choose, pattern=filter_chose),
            CallbackQueryHandler(other_city, pattern='^other_city$'),
            CallbackQueryHandler(main_menu, pattern='^menu$'),
            CallbackQueryHandler(other_menu, pattern='^other_menu$'),
        ],
        TYPING: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, save_text)
        ],

        MAIN_MENU: [
            CallbackQueryHandler(
                main_menu,
            ),
        ]
    },
    fallbacks=[MessageHandler(filters.Regex(
        "^Done$"), start)],
)
