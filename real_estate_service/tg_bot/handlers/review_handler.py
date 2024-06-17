from asgiref.sync import sync_to_async
from django.db.models import Case, CharField, F, Value, When
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from object.models import Realty
from reviews.models import Review
from tg_bot.middleware.check_tg_user import is_user_blocked
from user.models import TelegramUser

ASK_FOR_REVIEW = 1


@sync_to_async
def save_review(realty_id, tg_user_id, text):
    """Handler for saving the reviews"""
    realty = Realty.objects.filter(id=realty_id).first()
    if realty is None:
        return None
    author = TelegramUser.objects.filter(tg_id=tg_user_id).first()
    if author is None:
        return None
    Review.objects.create(
        real_estate=realty,
        author=author,
        text=text,
        status=Review.ReviewStatus.PENDING,
    )
    return True


@sync_to_async
def get_all_reviews_for_realty(realty_id):
    """Handler for getting all reviews for specific realty"""
    realty = Realty.objects.filter(id=realty_id).first()
    if not realty:
        return {"error": "Недвижимость не найдена"}

    reviews = (
        realty.reviews.select_related("author")
        .filter(status=Review.ReviewStatus.APPROVED)
        .order_by("-created_at")
        .annotate(
            author_name=Case(
                When(
                    author__isnull=True,
                    then=Value("Анонимно", output_field=CharField()),
                ),
                default=F("author__username"),
                output_field=CharField(),
            )
        )
        .values("author_name", "text")
    )

    return list(reviews)


async def receive_review(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handler for receiving the review"""
    tg_user_id = update.message.from_user.id
    if await is_user_blocked(tg_user_id):
        await update.message.reply_text(
            "⚠️ <b>Вы были заблокированы. Обратитесь к администратору!</b>",
            parse_mode="HTML",
        )
        return ConversationHandler.END

    realty_id = context.user_data.get("current_realty_id")
    text = update.message.text

    if realty_id:
        await save_review(realty_id, tg_user_id, text)
        await update.message.reply_text("Ваш отзыв отправлен на модерацию.")
        context.user_data["current_realty_id"] = None
    else:
        await update.message.reply_text("Недвижимость не найдена.")

    return ConversationHandler.END


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handler for for chosing the correct button"""
    query = update.callback_query
    await query.answer()

    tg_user_id = query.from_user.id
    if await is_user_blocked(tg_user_id):
        await query.message.reply_text(
            "⚠️ <b>Вы были заблокированы. Обратитесь к администратору!</b>",
            parse_mode="HTML",
        )
        return ConversationHandler.END

    if query.data.startswith("review_"):
        realty_id = query.data.split("_")[1]
        context.user_data["current_realty_id"] = realty_id
        await query.message.reply_text("Пожалуйста, напишите ваш отзыв.")
        return ASK_FOR_REVIEW

    elif query.data.startswith("view_reviews_"):
        realty_id = query.data.split("_")[2]
        reviews = await get_all_reviews_for_realty(realty_id)

        if reviews:
            if "error" in reviews:
                await query.message.reply_text(reviews["error"])
            else:
                reviews_text = "\n\n".join(
                    [
                        (f"Автор: {review['author_name']}\n"
                         f"Отзыв: {review['text']}")
                        for review in reviews
                    ]
                )
                await query.message.reply_text(reviews_text)
        else:
            await query.message.reply_text("Нет отзывов для этого объекта.")

    return ConversationHandler.END
