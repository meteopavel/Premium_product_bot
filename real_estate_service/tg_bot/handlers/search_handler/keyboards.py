from django.db import models
from telegram import InlineKeyboardButton, Update
from telegram.ext import ContextTypes

from object.models import BaseIntervals, City
from tg_bot.middleware.check_tg_user import is_user_subscribed
from .constants import MAIN_FIELDS, OTHER_FIELDS, MAX_MENU_ITEMS


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
                InlineKeyboardButton("Прочее", callback_data="other"),
            ]
        )
        keyboard.append(
            [
                InlineKeyboardButton(
                    "🤔 Показать результат", callback_data="represent_results"
                )
            ]
        )
    else:
        keyboard.append(
            [
                InlineKeyboardButton("Прочее", callback_data="other"),
                InlineKeyboardButton(
                    "🤔 Показать результат", callback_data="represent_results"
                ),
            ]
        )
    is_subscribed = await is_user_subscribed(update.effective_chat.id)
    if is_subscribed:
        keyboard.append(
            [
                InlineKeyboardButton(
                    "✅Отписаться", callback_data="subscribe_yes"
                )
            ]
        )
    else:
        keyboard.append(
            [
                InlineKeyboardButton(
                    "☐ Подписаться", callback_data="subscribe_no"
                )
            ]
        )
    return keyboard


def other_keyboard(
    context: ContextTypes.DEFAULT_TYPE,
) -> list[list[InlineKeyboardButton]]:
    keyboard = []
    for field in OTHER_FIELDS:
        keyboard.append(
            [InlineKeyboardButton(OTHER_FIELDS[field], callback_data=field)]
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
                InlineKeyboardButton(
                    "📘 Вернуться в меню", callback_data="return_to_main"
                ),
            ]
        )
    else:
        keyboard.append(
            [
                InlineKeyboardButton(
                    "📘 Вернуться в меню", callback_data="return_to_main"
                ),
            ]
        )

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
    keyboard.append(
        [InlineKeyboardButton("📘 Вернутся в меню", callback_data="menu")]
    )
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
        return [
            [
                InlineKeyboardButton(
                    "Интервалы не настроены, вернутся в главное меню",
                    callback_data="menu",
                )
            ],
        ]
    keyboard.append(
        [InlineKeyboardButton("📘 Вернутся в меню", callback_data="menu")]
    )
    return keyboard


REPRESENT_RESULTS_KEYBOARD = [
    [InlineKeyboardButton("Посмотрел", callback_data="Посмотрел")],
]

PUBLISH_DATE_KEYBOARD = [
    [InlineKeyboardButton("Сегодняшние", callback_data="1")],
    [InlineKeyboardButton("За неделю", callback_data="7")],
    [InlineKeyboardButton("За месяц", callback_data="31")],
    [InlineKeyboardButton("За полгода", callback_data="184")],
]


async def send_citys_keyboard(
    citys: list[dict] = None,
    page: int = None
) -> list[list[InlineKeyboardButton]]:
    if not citys:
        keyboard = [
            [InlineKeyboardButton("📘 выйти", callback_data="main_menu")],
        ]
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
                "⬅️", callback_data=f"page_{page-1}"
            )
        )
    if end_index < len(citys):
        keyboard[-1].append(InlineKeyboardButton(
            "➡️", callback_data=f"page_{page+1}"))
    keyboard.append(
        [InlineKeyboardButton("📘 Вернутся", callback_data="main_menu")]
    )
    return keyboard


def send_page_keyboard(page, length, pk):
    keyboard = []
    if page > 0:
        keyboard.append(
            InlineKeyboardButton("⬅️", callback_data=f"page_{page-1}")
        )
    if page + 1 < length:
        keyboard.append(
            InlineKeyboardButton("➡️", callback_data=f"page_{page+1}")
        )
    keyboard.append(InlineKeyboardButton("🏁 Выйти", callback_data="cancel"))
    keyboard.append(
        InlineKeyboardButton("📘 Поиск", callback_data="return_to_main"),
    )
    realty_button = [
        InlineKeyboardButton("🔍 Посмотреть", callback_data="realty_" + str(pk))
    ]
    keyboard = [keyboard]
    keyboard.append(realty_button)
    return keyboard
