from django.db import models
from telegram import (
    KeyboardButton, InlineKeyboardButton, ReplyKeyboardMarkup, Update
)
from telegram.ext import ContextTypes

from object.models import City
from tg_bot.middleware.check_tg_user import is_user_subscribed
from tg_bot.models import BaseIntervals, DateInterval
from .constants import MAIN_FIELDS, OTHER_FIELDS, MAX_MENU_ITEMS

NO_INTERVALS_KEYBOARD = [
    [
        InlineKeyboardButton(
            "Интервалы не настроены, вернутся в главное меню",
            callback_data="main_menu",
        )
    ],
]
RETURN_TO_MAIN_BUTTON = InlineKeyboardButton(
    "📘 Вернуться в меню", callback_data="main_menu"
)


async def main_keyboard(
    context: ContextTypes.DEFAULT_TYPE, update: Update
) -> list[list[InlineKeyboardButton]]:
    keyboard = []
    for field in MAIN_FIELDS:
        keyboard.append(
            [InlineKeyboardButton(MAIN_FIELDS[field], callback_data=field)]
        )
    is_search_data = False
    for field in MAIN_FIELDS | OTHER_FIELDS:
        if field in context.user_data and field != "location__city":
            is_search_data = True
            break
    if is_search_data:
        keyboard.append(
            [
                InlineKeyboardButton(
                    "🧽 Очистить фильтры", callback_data="refresh_all"
                ),
                InlineKeyboardButton("➕ Прочие фильтры", callback_data="other"),
            ]
        )
        keyboard.append(
            [
                InlineKeyboardButton(
                    "🕵🏻 Показать результат", callback_data="represent_results"
                )
            ]
        )
    else:
        keyboard.append(
            [
                InlineKeyboardButton("➕ Прочие фильтры", callback_data="other"),
                InlineKeyboardButton(
                    "🕵🏻 Показать результат", callback_data="represent_results"
                ),
            ]
        )
    is_subscribed = await is_user_subscribed(update.effective_chat.id)
    if is_subscribed:
        keyboard.append(
            [
                InlineKeyboardButton(
                    "❌ Отписаться от рассылки", callback_data="subscribe_yes"
                )
            ]
        )
    else:
        keyboard.append(
            [
                InlineKeyboardButton(
                    "✅ Подписаться на рассылку", callback_data="subscribe_no"
                )
            ]
        )
    keyboard.append([
        InlineKeyboardButton("🏁 Закончить поиск", callback_data="cancel")
    ])
    return keyboard


def other_keyboard(
    context: ContextTypes.DEFAULT_TYPE,
) -> list[list[InlineKeyboardButton]]:
    keyboard = []
    for field in OTHER_FIELDS:
        keyboard.append(
            [InlineKeyboardButton(OTHER_FIELDS[field], callback_data=field)]
        )
    keyboard.append(
        [InlineKeyboardButton(
            "🕵🏻 Показать результат", callback_data="represent_results"
        )]
    )
    is_search_data = False
    for field in OTHER_FIELDS:
        if field in context.user_data:
            is_search_data = True
            break
    if is_search_data:
        keyboard.append(
            [
                InlineKeyboardButton(
                    "🧽 Сбросить", callback_data="refresh_other"
                ),
                RETURN_TO_MAIN_BUTTON
            ]
        )
    else:
        keyboard.append([RETURN_TO_MAIN_BUTTON])

    return keyboard


async def all_obj_keyboard(
    model: models.Model,
) -> list[list[InlineKeyboardButton]]:
    keyboard = []
    async for object in model.objects.all().values_list("name", "pk"):
        data = {"name": object[0], "pk": object[1]}
        keyboard.append(
            [InlineKeyboardButton(data["name"], callback_data=data["pk"])]
        )
    keyboard.append([RETURN_TO_MAIN_BUTTON])
    return keyboard


async def location__city_keyboard() -> list[list[InlineKeyboardButton]]:
    """Создает клавиатуру из основных городов"""
    keyboard = []
    async for city in City.objects.filter(is_in_main_menu=True).values_list(
        "name", "pk"
    ):
        city_dic = {"name": city[0], "pk": city[1]}
        keyboard.append(
            [
                InlineKeyboardButton(
                    city_dic["name"], callback_data=city_dic["pk"]
                )
            ]
        )
    keyboard.append(
        [
            InlineKeyboardButton(
                "Города нет в списке. Выбрать другой.",
                callback_data="city_typing",
            )
        ]
    )
    return keyboard


async def interval_keyboard(
    model: BaseIntervals,
) -> list[list[InlineKeyboardButton]]:
    keyboard = []
    async for interval in model.objects.all():
        string = f"{interval.minimum}-{interval.maximum}"
        keyboard.append([InlineKeyboardButton(string, callback_data=string)])

    if not keyboard:
        return NO_INTERVALS_KEYBOARD

    keyboard.append([RETURN_TO_MAIN_BUTTON])
    return keyboard


async def publish_date_keyboard():
    keyboard = []
    async for interval in DateInterval.objects.all():
        string = f"{interval.name}"
        keyboard.append(
            [InlineKeyboardButton(
                string,
                callback_data=str(interval.date_interval)
            )])
    if not keyboard:
        return NO_INTERVALS_KEYBOARD
    keyboard.append([RETURN_TO_MAIN_BUTTON])
    return keyboard


async def send_citys_keyboard(
    citys: list[dict] = None,
    page: int = None
) -> list[list[InlineKeyboardButton]]:
    if not citys:
        keyboard = [[RETURN_TO_MAIN_BUTTON]]
        return keyboard
    keyboard = []
    start_index = page * MAX_MENU_ITEMS
    end_index = start_index + MAX_MENU_ITEMS
    items = citys[start_index:end_index]
    for city in items:
        text = city["name"]
        if city.get("region"):
            text += ":" + str(city["region"])
        text += ":" + str(city["country"])
        keyboard.append(
            [
                InlineKeyboardButton(
                    text,
                    callback_data=city["pk"],
                )
            ]
        )
    keyboard.append([])
    if page > 0:
        keyboard[-1].append(
            InlineKeyboardButton(
                "⬅️ Предыдущее", callback_data=f"page_{page-1}"
            )
        )
    if end_index < len(citys):
        keyboard[-1].append(InlineKeyboardButton(
            "Следующее ➡️", callback_data=f"page_{page+1}"))
    keyboard.append(
        [InlineKeyboardButton("📘 Вернуться", callback_data="main_menu")]
    )
    return keyboard


def send_page_keyboard(page, length, pk):
    keyboard = []

    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(
            InlineKeyboardButton("⬅️ Предыдущее",
                                 callback_data=f"page_{page - 1}")
        )
    if page + 1 < length:
        navigation_buttons.append(
            InlineKeyboardButton("Следующее ➡️",
                                 callback_data=f"page_{page + 1}")
        )

    if navigation_buttons:
        keyboard.append(navigation_buttons)

    action_buttons = [
        InlineKeyboardButton("📘 Новый поиск", callback_data="main_menu"),
        InlineKeyboardButton("🏁 Закончить поиск", callback_data="cancel")
    ]
    keyboard.append(action_buttons)

    realty_button = [
        InlineKeyboardButton("🔍 Посмотреть подробности",
                             callback_data="realty_" + str(pk))
    ]
    keyboard.append(realty_button)

    return keyboard
