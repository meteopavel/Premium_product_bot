from telegram.ext import ContextTypes

from .constants import MAIN_FIELDS, OTHER_FIELDS


def user_data_as_text(context: ContextTypes.DEFAULT_TYPE) -> str:
    text = 'Вот:'
    join_fields = MAIN_FIELDS | OTHER_FIELDS
    for field in join_fields:
        if field in context.user_data:
            text += f'\n{join_fields[field]}: {context.user_data[field]}'
    return text
