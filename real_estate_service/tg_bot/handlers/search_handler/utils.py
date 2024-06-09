from datetime import datetime, timedelta

from telegram import Update
from telegram.ext import ContextTypes


async def edit_or_send(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        text,
        reply_markup
) -> None:
    """Проверит запрос. Если он есть - обновит сообщение. 
    Если нет то просто отправит"""
    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_text(
            text=text,
            reply_markup=reply_markup
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=reply_markup
        )
# Вспомогательные штучки
search_fields: list[str] = [
    'location__city', 'area', 'price', 'category',
    'publish_date', 'condition', 'building_type', 'text'
]
foregin_fields = ['location__city', 'category', 'condition', 'building_type',]
integer_fields = ['area', 'price']
datetime_field = 'publish_date'
text_field = 'text'


def filter_args(
        context: ContextTypes.DEFAULT_TYPE
) -> dict:
    """Формирует словарь аргументов для запроса к БД
    через ORM."""
    args = {}
    for field in foregin_fields:
        if field in context.user_data:
            query = field + '__name'
            data = context.user_data[field]
            args[query] = data
    for field in integer_fields:
        if field in context.user_data:
            query = field + '__lte'
            minimum = context.user_data[field].split('-')[0]
            maximum = context.user_data[field].split('-')[1]
            args[query] = maximum
            query = field + '__gt'
            args[query] = minimum
    if datetime_field in context.user_data:
        query = datetime_field + '__range'
        days_to_subtract = int(context.user_data[datetime_field])
        end_date = datetime.today()
        start_date = end_date - timedelta(days=days_to_subtract)
        args[query] = (start_date, end_date)
    if text_field in context.user_data:
        query = text_field + '__icontains'
        data = context.user_data[field]
        args[query] = data
    return args
