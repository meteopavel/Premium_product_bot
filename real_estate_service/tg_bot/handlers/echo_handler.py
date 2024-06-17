from telegram import Update
from telegram.ext import ContextTypes

from tg_bot.middleware import is_user_blocked


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    user_id = update.effective_user.id
    if await is_user_blocked(user_id):
        await update.message.reply_text(
            "⚠️ <b>Вы были заблокированы. Обратитесь к администратору!</b>",
            parse_mode="HTML",
        )
        return
    await update.message.reply_text(update.message.text)
