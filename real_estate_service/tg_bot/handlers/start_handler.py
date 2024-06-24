from telegram import Update
from telegram.ext import ContextTypes, Filters, dispatcher
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, MessageHandler, CommandHandler

from .base_utils import get_or_create_telegram_user

SEARCH, MY_FAVORITES, CONTACTS = range(3)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for start button"""
    tg_id = update.message.from_user.id
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    username = update.message.from_user.username

    tg_user, created = await get_or_create_telegram_user(
        tg_id, first_name, last_name, username
    )
    text = ""
    if created:
        text = f"Привет {username}\n"
    else:
        text = f"С возвращением, {username}\n"

    info_text = (
        "Введите команду:\n/search - чтобы начать поиск"
        " недвижимости;\n/my_favorites - чтобы посмотреть все ваши"
        " избранные;\n/contacts - наши контакты;\n/stop -"
        " чтобы удалиться из бота;"
    )
    full_text = text + info_text
    await update.message.reply_html(text=full_text)

    keyboard = [['/search', '/my_favorites'], ['/contacts', '/stop']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_html(text=full_text, reply_markup=reply_markup)
    return SEARCH


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Обработка команды /search
    # Ваша логика обработки команды /search
    return MY_FAVORITES


async def my_favorites(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Обработка команды /my_favorites
    # Ваша логика обработки команды /my_favorites
    return CONTACTS


async def contacts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Обработка команды /contacts
    # Ваша логика обработки команды /contacts
    return ConversationHandler.END


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Обработка команды /stop
    # Ваша логика обработки команды /stop
    return ConversationHandler.END

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        SEARCH: [MessageHandler(Filters.regex('^/search$'), search)],
        MY_FAVORITES: [MessageHandler(Filters.regex('^/my_favorites$'), my_favorites)],
        CONTACTS: [MessageHandler(Filters.regex('^/contacts$'), contacts)],
    },
    fallbacks=[CommandHandler('stop', stop)],
)

# Добавляем ConversationHandler в диспетчер обновлений
dispatcher.add_handler(conv_handler)
