from asgiref.sync import sync_to_async
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Update,
)
from telegram.ext import ContextTypes, ConversationHandler

from object.models import (
    BuldingType,
    Category,
    City,
    Condition,
    Realty,
)
from tg_bot.models import PriceIntervals, AreaIntervals
from tg_bot.handlers.show_realty import show_realty
from tg_bot.middleware import is_user_blocked
from tg_bot.handlers.base_utils import get_country_from_city
from .constants import (
    CHOOSE,
    CITY_TYPING,
    FIELDS,
    LOGO_URL_ABSOLUTE,
    LOGO_URL_RELATIVE,
    MAIN_FIELDS,
    OTHER_FIELDS,
    REPRESENT,
    REPRESENT_CITYS,
    SAVE_CHOOSE,
    TYPING,
)
from .keyboards import (
    publish_date_keyboard,
    all_obj_keyboard,
    interval_keyboard,
    location__city_keyboard,
    main_keyboard,
    other_keyboard,
    send_citys_keyboard,
    send_page_keyboard,
)
from .keyboards import RETURN_TO_MAIN_BUTTON
from .texts import user_data_as_text
from .utils import (
    edit_or_send,
    filter_args,
    insert_object_card,
    save_is_subscribed,
    save_search_parameters,
    unpack_search_parameters,
)


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Основное меню"""
    user_id = update.effective_user.id
    if await is_user_blocked(user_id):
        await update.message.reply_text(
            "⚠️ <b>Вы были заблокированы. Обратитесь к администратору!</b>",
            parse_mode="HTML",
        )
        return ConversationHandler.END
    if "search" not in context.user_data:
        if not await unpack_search_parameters(update, context):
            return await cancel(update, context)
    if "location__city" not in context.user_data:
        return await location__city(update, context)
    if "all_citys" in context.user_data:
        del context.user_data["all_citys"]
    if "suitable_realtys" in context.user_data:
        del context.user_data["suitable_realtys"]
    context.user_data["search"] = True
    reply_markup = InlineKeyboardMarkup(await main_keyboard(context, update))
    main_text = await user_data_as_text(context)
    await edit_or_send(update, context, main_text, reply_markup)
    return CHOOSE


async def location__city(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Меню выбора города"""
    reply_markup = InlineKeyboardMarkup(await location__city_keyboard())
    context.user_data["choose"] = "location__city"
    if "location__city" in context.user_data:
        city = await sync_to_async(
            lambda: City.objects.filter(id=context.user_data["location__city"])
            .values_list("name")
            .first()[0]
        )()
        city_text = f"Выбранный ранее город: {city}"
    else:
        city_text = "Выбери город!"
    await edit_or_send(update, context, city_text, reply_markup)
    return SAVE_CHOOSE


async def city_typing(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    text: str = None
) -> int:
    """Меню выбора города, если его нет в списке основных городов."""
    if not text:
        text = "Напишите название города."
        reply_markup = None
    else:
        reply_markup = InlineKeyboardMarkup(await send_citys_keyboard())
    await edit_or_send(update, context, text, reply_markup)
    return CITY_TYPING


MAX_CITYS = 60


async def other_citys_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    page = 0
    citys = []
    async for city in City.objects.filter(name__icontains=text):
        country = await get_country_from_city(city)
        citys.append(
            {"name": city.name,
             "region": city.district,
             "country": country,
             "pk": city.pk}
        )
    if len(citys) > MAX_CITYS:
        citys = []
    context.user_data["all_citys"] = citys
    return await send_citys(update, context, page)


async def send_citys(update: Update, context: ContextTypes.DEFAULT_TYPE, page):
    citys = context.user_data["all_citys"]
    if citys:
        message_text = "вот:"
    else:
        text = "Нет ожидаемого результата. Попробуйте еще!"
        return await city_typing(update, context, text)
    reply_markup = InlineKeyboardMarkup(await send_citys_keyboard(citys, page))
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=LOGO_URL_RELATIVE,
        caption=message_text,
        reply_markup=reply_markup,
    )
    return REPRESENT_CITYS


async def rep_button2(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    query = update.callback_query
    await query.answer()
    query_data = query.data

    if query_data.startswith("page_"):
        page = int(query_data.split("_")[1])
        await send_citys(update, context, page)
    if query_data.startswith("main_menu"):
        await main_menu(update, context)


async def rent_or_sell(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Меню выбора типа объявления."""
    query = update.callback_query
    await query.answer()
    reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Аренда", callback_data="rent")],
            [InlineKeyboardButton("Продажа", callback_data="sell")],
            [RETURN_TO_MAIN_BUTTON],
        ]
    )
    context.user_data["choose"] = "rent_or_sell"
    text = "Аренда/Продажа"
    await insert_object_card(query, LOGO_URL_ABSOLUTE, text, reply_markup)
    return SAVE_CHOOSE


async def area(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Выбор диапазона площади"""
    query = update.callback_query
    await query.answer()
    reply_markup = InlineKeyboardMarkup(await interval_keyboard(AreaIntervals))
    context.user_data["choose"] = "area"
    text = "Выбери площадь"
    await insert_object_card(query, LOGO_URL_ABSOLUTE, text, reply_markup)
    return SAVE_CHOOSE


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Меню выбора диапазона цены."""
    query = update.callback_query
    await query.answer()
    reply_markup = InlineKeyboardMarkup(
        await interval_keyboard(PriceIntervals)
    )
    context.user_data["choose"] = "price"
    text = "Выбери цену"
    await insert_object_card(query, LOGO_URL_ABSOLUTE, text, reply_markup)
    return SAVE_CHOOSE


async def category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Меню выбора категории"""
    query = update.callback_query
    await query.answer()
    reply_markup = InlineKeyboardMarkup(await all_obj_keyboard(Category))
    context.user_data["choose"] = "category"
    if "category" in context.user_data:
        text = f'Выбранная ранее категория:{context.user_data["category"]}'
    else:
        text = "Выбери категорию!"
    await insert_object_card(query, LOGO_URL_ABSOLUTE, text, reply_markup)
    return SAVE_CHOOSE


async def refresh_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Удалить все данные, кроме города"""
    query = update.callback_query
    await query.answer()
    for field in MAIN_FIELDS | OTHER_FIELDS:
        if field in context.user_data and field != "location__city":
            del context.user_data[field]
    return await main_menu(update, context)


async def represent_results(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    realtys = []
    async for realty in Realty.objects.filter(**filter_args(context.user_data)):
        realtys.append(
            {
                "title": realty.title,
                "id": realty.id,
                "area": realty.area,
                "price": realty.price,
                "image": realty.image,
                "is_active": realty.is_active,
            }
        )
    context.user_data["suitable_realtys"] = realtys

    if not realtys:
        text = "🤷‍♂️ Ничего подходящего."
        keyboard = [[RETURN_TO_MAIN_BUTTON]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await insert_object_card(query, LOGO_URL_ABSOLUTE, text, reply_markup)
        return

    page = context.user_data.get("page", 0)

    if 0 <= page < len(realtys):
        realty = realtys[page]
        realty_id = realty["id"]

        if not realty["is_active"]:
            text = (
                f"Объект недвижимости: {realty['title']}\n"
                "Этот объект был удален администратором."
            )
        else:
            text = (
                f"Объект недвижимости: {realty['title']}\n"
                f"Площадь: {realty['area']} кв.м\n"
                f"Цена: {realty['price']} руб."
            )

        keyboard = send_page_keyboard(page, len(realtys), realty_id)
        reply_markup = InlineKeyboardMarkup(keyboard)
        if realty["image"]:
            await insert_object_card(query, realty["image"], text, reply_markup)
        else:
            await insert_object_card(query, LOGO_URL_ABSOLUTE, text, reply_markup)
    else:
        text = "🤷‍♂️ Индекс страницы вне диапазона."
        keyboard = [
            [RETURN_TO_MAIN_BUTTON]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await insert_object_card(query, LOGO_URL_ABSOLUTE, text, reply_markup)
    return CHOOSE



async def realty_callback_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    await show_realty(update, context)


async def page_navigation_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    page = int(query.data.split("_")[1])
    context.user_data["page"] = page
    await represent_results(update, context)


async def back_to_list_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    await represent_results(update, context)


async def cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_media(
        media=InputMediaPhoto(
            media=LOGO_URL_ABSOLUTE, caption="Поиск отменён."
        ),
    )


async def send_page(update: Update, context: ContextTypes.DEFAULT_TYPE, page):
    realtys = context.user_data["suitable_realtys"]
    realty = realtys[page]
    text = (f'вот:\n{realty["title"]}\n{FIELDS["area"]}: '
            f'{realty["area"]}\n{FIELDS["price"]}: {realty["price"]}\n')
    pk = realty["id"]
    reply_markup = InlineKeyboardMarkup(
        send_page_keyboard(page, len(realtys), pk)
    )
    query = update.callback_query
    await query.answer()
    await insert_object_card(query, LOGO_URL_ABSOLUTE, text, reply_markup)
    return REPRESENT


async def rep_button(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    query = update.callback_query
    await query.answer()
    query_data = query.data

    page = int(query_data.split("_")[1])
    await send_page(update, context, page)


async def other_menu(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Дополнительное меню параметров поиска"""
    reply_markup = InlineKeyboardMarkup(other_keyboard(context))
    text = await user_data_as_text(context)
    if not context.user_data.get("text_input"):
        await edit_or_send(update, context, text, reply_markup)
    else:
        await update.message.reply_photo(
            caption=text,
            photo=LOGO_URL_ABSOLUTE,
            reply_markup=reply_markup
        )
        del context.user_data["text_input"]
    return CHOOSE


async def publish_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Меню выбора периода даты публикации"""
    reply_markup = InlineKeyboardMarkup(await publish_date_keyboard())
    context.user_data["choose"] = "publish_date"
    query = update.callback_query
    text = "Выбери период публикации"
    await query.answer()
    await insert_object_card(query, LOGO_URL_ABSOLUTE, text, reply_markup)
    return SAVE_CHOOSE


async def condition(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Меню выбора состояния помещения"""
    query = update.callback_query
    await query.answer()
    reply_markup = InlineKeyboardMarkup(await all_obj_keyboard(Condition))
    context.user_data["choose"] = "condition"
    if "condition" in context.user_data:
        text = ('Выбранное ранее состояние помещений'
                f':{context.user_data["condition"]}')
    else:
        text = "Какое состояние помещений вас устроит?"
    await insert_object_card(query, LOGO_URL_ABSOLUTE, text, reply_markup)
    return SAVE_CHOOSE


async def building_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Меню выбора типа здания"""
    query = update.callback_query
    await query.answer()
    reply_markup = InlineKeyboardMarkup(await all_obj_keyboard(BuldingType))
    context.user_data["choose"] = "building_type"
    if "building_type" in context.user_data:
        text = (
            f'Выбранный ранее тип здания:{context.user_data["building_type"]}'
        )
    else:
        text = "Ваберите тип здания, в которм нужны помещения."
    await insert_object_card(query, LOGO_URL_ABSOLUTE, text, reply_markup)
    return SAVE_CHOOSE


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Меню выбора статуса объявления."""
    query = update.callback_query
    await query.answer()
    reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Актуально", callback_data="relevant")],
            [InlineKeyboardButton(
                "Неактуально", callback_data="not_relevant")],
            [RETURN_TO_MAIN_BUTTON],
        ]
    )
    context.user_data["choose"] = "status"
    text = "Актуально/Неактуально"
    await insert_object_card(query, LOGO_URL_ABSOLUTE, text, reply_markup)
    return SAVE_CHOOSE


async def text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt user to input data for selected feature."""
    context.user_data["choose"] = update.callback_query.data
    text = "Введите текс, которой должен быть в объявлении"
    query = update.callback_query
    await query.answer()
    await query.edit_message_media(
        media=InputMediaPhoto(media=LOGO_URL_ABSOLUTE, caption=text),
    )
    return TYPING


async def save_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save text for feature and return to other menu."""
    user_data = context.user_data
    user_data[user_data["choose"]] = update.message.text
    context.user_data["text_input"] = True
    return await other_menu(update, context)


async def save_choose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    query = update.callback_query
    await query.answer()
    user_data[user_data["choose"]] = query.data
    if user_data["choose"] in MAIN_FIELDS:
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
    if "search" in context.user_data:
        del context.user_data["search"]
    if await save_search_parameters(update, context):
        text = "Поиск окончен."
    else:
        text = "Вы не зарегистрированны. Пожалуйста, введите /start"
    await edit_or_send(update, context, text)
    return ConversationHandler.END


async def subscribe(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    query = update.callback_query
    await query.answer()
    is_subscribed = False
    if query.data.split("_")[-1] == "no":
        is_subscribed = True
    if not is_subscribed:
        await save_search_parameters(update, context)
    tg_id = update.effective_chat.id
    await save_is_subscribed(tg_id, is_subscribed)
    await main_menu(update, context)
