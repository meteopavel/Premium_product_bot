from telegram.ext import (
    ConversationHandler,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters
)

from .callbacks import (
    main_menu, location__city, category, price,
    other_menu, area, publish_date,
    condition, represent_results, refresh_all, refresh_other,
    save_choose, condition, building_type, text,
    publish_date, save_text, rep_button, city_typing,
    rep_button2, other_citys_list, cancel
)
from .constants import REPRESENT, CHOOSE, \
    TYPING, SAVE_CHOOSE, CITY_TYPING, \
    MAIN_FIELDS, OTHER_FIELDS, REPRESENT_CITYS
from .filters import filter_main_menu, filter_rep_city
from .. import show_realty

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
                save_choose, pattern=filter_main_menu),
            CallbackQueryHandler(city_typing, pattern='^city_typing$'),
            CallbackQueryHandler(main_menu, pattern='^menu$'),
            CallbackQueryHandler(other_menu, pattern='^other_menu$'),
        ],
        TYPING: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, save_text)
        ],
        CITY_TYPING: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, other_citys_list)
        ],
        REPRESENT: [
            CallbackQueryHandler(rep_button, pattern='^(page)'),
            CallbackQueryHandler(main_menu, pattern='^main_menu$'),
            CallbackQueryHandler(show_realty.show_realty, pattern='^realty_')
        ],
        REPRESENT_CITYS: [
            CallbackQueryHandler(rep_button2, pattern='^(page|main_menu)'),
            CallbackQueryHandler(save_choose, pattern=filter_rep_city),
            CallbackQueryHandler(city_typing, pattern='^city_typing$')

        ]
    },
    fallbacks=[
        CommandHandler('cancel', cancel),
        CommandHandler('start', cancel),
        CommandHandler('stop', cancel),
        CommandHandler('my_favorites', cancel),
        CallbackQueryHandler(cancel, pattern='^cancel$')
    ],
)
