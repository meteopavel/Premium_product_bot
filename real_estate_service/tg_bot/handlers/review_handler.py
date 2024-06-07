from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, ContextTypes
from user.models import TelegramUser
from reviews.models import Review
from object.models import Realty
from asgiref.sync import sync_to_async

@sync_to_async
def save_review(realty_id, tg_user_id, text):
    realty = Realty.objects.get(id=realty_id)
    author = TelegramUser.objects.get(tg_id=tg_user_id)
    Review.objects.create(real_estate=realty, author=author, text=text, status=Review.ReviewStatus.PENDING)

@sync_to_async
def get_all_reviews_for_realty(realty_id):
    realty = Realty.objects.get(id=realty_id)
    reviews = realty.reviews.select_related('author').filter(status=Review.ReviewStatus.APPROVED).order_by('-created_at')
    return [
        {
            'author': review.author.username if review.author else 'Анонимно',
            'text': review.text
        }
        for review in reviews
    ]

async def receive_review(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tg_user_id = update.message.from_user.id
    realty_id = context.user_data.get('current_realty_id')
    text = update.message.text

    if realty_id:
        await save_review(realty_id, tg_user_id, text)
        await update.message.reply_text('Ваш отзыв отправлен на модерацию.')
        context.user_data['current_realty_id'] = None
    else:
        await update.message.reply_text('Произошла ошибка, попробуйте еще раз.')

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data.startswith("review_"):
        realty_id = query.data.split("_")[1]
        context.user_data['current_realty_id'] = realty_id
        await query.message.reply_text('Пожалуйста, напишите ваш отзыв.')

    elif query.data.startswith("view_reviews_"):
        realty_id = query.data.split("_")[2]
        reviews = await get_all_reviews_for_realty(realty_id)

        if reviews:
            reviews_text = "\n\n".join([f"Автор: {review['author']}\nОтзыв: {review['text']}" for review in reviews])
            await query.message.reply_text(reviews_text)
        else:
            await query.message.reply_text('Нет отзывов для этого объекта.')
