from telegram import Update

from telegram.ext import ContextTypes, ConversationHandler

from object.models import Realty


async def show_realty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    pk: int = int(query.data.split('_')[-1])
    realty = await Realty.objects.filter(pk=pk).afirst()
    await query.edit_message_text(text=str(realty))
    return ConversationHandler.END
