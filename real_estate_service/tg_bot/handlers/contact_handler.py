from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import ContextTypes

from .base_utils import get_admin_is_staff, get_admin_is_superuser


async def contacts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for contact button"""
    text = (
        "Мы рады, что вы пользуетесь нашим ботом.\nЕсли вам необходима "
        "помощь, обратитесь к администраторам:\n"
    )
    staff_list = await get_admin_is_staff()
    superuser_list = await get_admin_is_superuser()
    all_admins = set(staff_list + superuser_list)
    for admin in all_admins:
        tg_username = "Админ не имеет профиль в телеграмм"
        admin_tg_user = await sync_to_async(
            lambda: admin.tg_user if hasattr(admin, "tg_user") else None
        )()
        if admin_tg_user:
            tg_username = f"@{admin_tg_user.username}"
        text += (
            f"{admin.first_name} {admin.last_name} - "
            f"{admin.email} - {tg_username}\n"
        )
    await update.message.reply_html(text=text)
