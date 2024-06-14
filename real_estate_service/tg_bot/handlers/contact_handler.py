from telegram import Update
from telegram.ext import ContextTypes

from .base_utils import get_admin_is_staff, get_admin_is_superuser


async def contacts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Мы рады, что вы пользуетесь нашим ботом.\nЕсли вам необходима "\
            "помощь, обратитесь к администраторам:\n"
    staff_list = await get_admin_is_staff()
    superuser_list = await get_admin_is_superuser()
    all_admins = set(staff_list + superuser_list)
    for admin in all_admins:
        text += f"{admin.first_name} {admin.last_name} - {admin.email}\n"
    await update.message.reply_html(text=text)