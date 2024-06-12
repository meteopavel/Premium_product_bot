from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from object.models import Realty
from tg_bot.handlers.search_handler.utils import save_search_parameters


async def show_realty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    pk: int = int(query.data.split('_')[-1])
    realty = await Realty.objects.filter(pk=pk).afirst()
    if 'search' in context.user_data:
        del context.user_data['search']
        await save_search_parameters(update, context)
    await query.edit_message_text(text=str(realty))
    return ConversationHandler.END
