from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes, ConversationHandler

from tg_bot.middleware import is_user_blocked
from object.models import (
    Realty,
    Category,
    Condition,
    BuldingType,
    City,
    AreaIntervals,
    PriceIntervals
)
from .constants import REPRESENT, CHOOSE, TYPING, SAVE_CHOOSE, MAIN_FIELDS, OTHER_FIELDS, CITY_TYPING, REPRESENT_CITYS, FIELDS
from .utils import (
    edit_or_send,
    filter_args,
    save_search_parameters,
    save_is_subscribed,
    unpack_search_parameters
)
from .keyboards import (
    location__city_keyboard, all_obj_keyboard,
    main_keyboard, other_keyboard,
    send_citys_keyboard, send_page_keyboard,
    interval_keyboard
)
from .keyboards import PUBLISH_DATE_KEYBOARD

from .texts import user_data_as_text


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Основное меню"""
    user_id = update.effective_user.id
    if await is_user_blocked(user_id):
        await update.message.reply_text(
            "⚠️ <b>Вы были заблокированы. Обратитесь к администратору!</b>",
            parse_mode='HTML'
        )
        return ConversationHandler.END
    if 'search' not in context.user_data:
        if not await unpack_search_parameters(update, context):
            return await cancel(update, context)
    if 'location__city' not in context.user_data:
        return await location__city(update, context)
    if 'all_citys' in context.user_data:
        del context.user_data['all_citys']
    if 'suitable_realtys' in context.user_data:
        del context.user_data['suitable_realtys']
    context.user_data['search'] = True
    reply_markup = InlineKeyboardMarkup(await main_keyboard(context, update))
    main_text = await user_data_as_text(context)
    await edit_or_send(update, context, main_text, reply_markup)
    return CHOOSE


async def location__city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Меню выбора города"""
    reply_markup = InlineKeyboardMarkup(await location__city_keyboard())
    context.user_data['choose'] = 'location__city'
    if 'location__city' in context.user_data:
        city_text = city_text = f'Выбранный ранее город: {
            context.user_data["location__city"]}'
    else:
        city_text = 'Выбери город!'
    await edit_or_send(update, context, city_text, reply_markup)
    return SAVE_CHOOSE


async def city_typing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Меню выбора города, если его нет в списке основных городов. """
    text = 'Напишите название города'
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text)
    return CITY_TYPING

MAX_CITYS = 60


async def other_citys_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    page = 0
    citys = []
    async for city in City.objects.filter(name__icontains=text):
        citys.append(
            {'name': city.name, 'region': city.district, 'pk': city.pk})
    if len(citys) > MAX_CITYS:
        citys = []
    context.user_data['all_citys'] = citys
    return await send_citys(update, context, page)


async def send_citys(update: Update, context: ContextTypes.DEFAULT_TYPE, page):
    citys = context.user_data['all_citys']
    if citys:
        message_text = 'вот:'
    else:
        message_text = 'Нет ожидаемого результата. Попробуйте еще!'
    reply_markup = InlineKeyboardMarkup(
        await send_citys_keyboard(citys, page)
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message_text,
        reply_markup=reply_markup)
    return REPRESENT_CITYS


async def rep_button2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    query_data = query.data

    if query_data.startswith('page_'):
        page = int(query_data.split('_')[1])
        await send_citys(update, context, page)
    if query_data.startswith('main_menu'):
        await main_menu(update, context)


async def area(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Выбор диапазона площади"""
    query = update.callback_query
    await query.answer()
    markup = InlineKeyboardMarkup(await interval_keyboard(AreaIntervals))
    context.user_data['choose'] = 'area'
    await query.edit_message_text(text='Выбери площадь', reply_markup=markup)
    return SAVE_CHOOSE


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Меню выбора диапазона цены."""
    query = update.callback_query
    await query.answer()
    markup = InlineKeyboardMarkup(await interval_keyboard(PriceIntervals))
    context.user_data['choose'] = 'price'
    await query.edit_message_text(text='Выбери цену', reply_markup=markup)
    return SAVE_CHOOSE


async def category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Меню выбора категории"""
    query = update.callback_query
    await query.answer()
    reply_markup = InlineKeyboardMarkup(await all_obj_keyboard(Category))
    context.user_data['choose'] = 'category'
    if 'category' in context.user_data:
        text = f'Выбранная ранее категория:{context.user_data["category"]}'
    else:
        text = "Выбери категорию!"
    await query.edit_message_text(text=text, reply_markup=reply_markup)
    return SAVE_CHOOSE


async def refresh_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Удалить все данные, кроме города"""
    query = update.callback_query
    await query.answer()
    for field in MAIN_FIELDS | OTHER_FIELDS:
        if field in context.user_data and field != 'location__city':
            del context.user_data[field]
    return await main_menu(update, context)


async def represent_results(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показать результаты поиска"""
    realtys = []
    async for realty in Realty.objects.filter(**filter_args(context.user_data)):
        realtys.append(
            {
                'title': realty.title,
                'id': realty.id,
                'area': realty.area,
                'price': realty.price,
            }
        )
    context.user_data['suitable_realtys'] = realtys
    if not realtys:
        text = 'Ничего подходящего=('
        query = update.callback_query
        await query.answer()
        keyboard = [
            [InlineKeyboardButton(
                'в главное меню', callback_data='main_menu')],
        ]
        markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=text,  reply_markup=markup)
    if realtys:
        page = 0
        await send_page(update=update, context=context, page=page)
    return REPRESENT


async def send_page(update: Update, context: ContextTypes.DEFAULT_TYPE, page):
    realtys = context.user_data['suitable_realtys']
    message_text = 'вот:\n'
    message_text += f'{realtys[page]["title"]}\n'
    message_text += f'{FIELDS["area"]}: {realtys[page]["area"]}\n'
    message_text += f'{FIELDS["price"]}: {realtys[page]["price"]}\n'
    pk = realtys[page]['id']
    reply_markup = InlineKeyboardMarkup(
        send_page_keyboard(page, len(realtys), pk))
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=message_text,
        reply_markup=reply_markup
    )
    return REPRESENT


async def rep_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    query_data = query.data

    page = int(query_data.split('_')[1])
    await send_page(update, context, page)


async def other_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Дополнительное меню параметров поиска"""
    reply_markup = InlineKeyboardMarkup(other_keyboard(context))
    text = await user_data_as_text(context)
    if not context.user_data.get('text_input'):
        await edit_or_send(update, context, text, reply_markup)
    else:
        await update.message.reply_text(
            text=text,
            reply_markup=reply_markup
        )
        del context.user_data['text_input']

    return CHOOSE


async def publish_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Меню выбора периода даты публикации"""
    markup = InlineKeyboardMarkup(PUBLISH_DATE_KEYBOARD)
    context.user_data['choose'] = 'publish_date'
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text='Выбери период публикации', reply_markup=markup)
    return SAVE_CHOOSE


async def condition(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Меню выбора состояния помещения"""
    query = update.callback_query
    await query.answer()
    reply_markup = InlineKeyboardMarkup(await all_obj_keyboard(Condition))
    context.user_data['choose'] = 'condition'
    if 'condition' in context.user_data:
        text = f'Выбранное ранее состояние помещений:{
            context.user_data["condition"]}'
    else:
        text = 'Какое состояние помещений вас устроит?'
    await query.edit_message_text(text=text, reply_markup=reply_markup)
    return SAVE_CHOOSE


async def building_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Меню выбора типа здания"""
    query = update.callback_query
    await query.answer()
    reply_markup = InlineKeyboardMarkup(await all_obj_keyboard(BuldingType))
    context.user_data['choose'] = 'building_type'
    if 'building_type' in context.user_data:
        text = f'Выбранный ранее тип здания:{
            context.user_data["building_type"]}'
    else:
        text = 'Ваберите тип здания, в которм нужны помещения.'
    await query.edit_message_text(text=text, reply_markup=reply_markup)
    return SAVE_CHOOSE


async def text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt user to input data for selected feature."""
    context.user_data['choose'] = update.callback_query.data
    text = 'Введите текс, которой должен быть в объявлении'

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text)
    return TYPING


async def save_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save text for feature and return to other menu."""
    user_data = context.user_data
    user_data[user_data['choose']] = update.message.text
    context.user_data['text_input'] = True
    return await other_menu(update, context)


async def save_choose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    query = update.callback_query
    await query.answer()
    user_data[user_data['choose']] = query.data
    if user_data['choose'] in MAIN_FIELDS:
        return await main_menu(update, context)
    return await other_menu(update, context)


async def refresh_other(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Удалить все данные, вводимые во вспмогатльном меню"""
    query = update.callback_query
    await query.answer()
    for field in OTHER_FIELDS:
        if field in context.user_data:
            del context.user_data[field]
    return await other_menu(update, context)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Выход из поиска"""
    if 'search' in context.user_data:
        del context.user_data['search']
    if await save_search_parameters(update, context):
        text = 'Поиск окончен.'
    else:
        text = 'Вы не зарегистрированны. Скомандуйте начать.'
    await edit_or_send(update, context, text)
    return ConversationHandler.END


async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    is_subscribed = False
    if query.data.split('_')[-1] == 'no':
        is_subscribed = True
    tg_id = update.effective_chat.id
    await save_is_subscribed(tg_id, is_subscribed)
    await main_menu(update, context)
