import os

from asgiref.sync import sync_to_async
from dotenv import load_dotenv
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

from object.models import Realty
from user.models import TelegramUser
from tg_bot.handlers.search_handler.constants import FIELDS, LOGO_URL_RELATIVE
from tg_bot.handlers.search_handler.utils import string_to_dict

load_dotenv()


def get_field_value(obj: Realty, field: str):
    attr_value = obj
    attr_value = getattr(attr_value, field, None)
    if attr_value is None:
        return None
    return attr_value


def get_filled_fields(obj: Realty, fields) -> dict:
    filled_fields = {}
    for field in fields:
        value = get_field_value(obj, field)
        if value is not None:
            filled_fields[field] = value
    return filled_fields


# Вспомогательные штучки
search_fields: list[str] = [
    "location__city",
    "area",
    "price",
    "category",
    "publish_date",
    "condition",
    "building_type",
    "text",
]
foregin_fields = [
    "category",
    "condition",
    "building_type",
]
integer_fields = ["area", "price"]
datetime_field = "publish_date"
text_fields = ["text"]


def compare_forgein(user_params: dict, forgein_data):
    if not user_params or not forgein_data:
        return True
    for field in forgein_data:
        if field in user_params and forgein_data[field] != str(
            user_params[field]
        ):
            return False
    return True


def compare_integer(user_params: dict, integer_data: dict):
    if not user_params or not integer_data:
        return True
    is_in_range = True
    for field in integer_data:
        if field in user_params:
            minimum = int(user_params[field].split("-")[0])
            maximum = int(user_params[field].split("-")[1])
            if not (
                integer_data[field] < maximum
                and integer_data[field] >= minimum
            ):
                is_in_range = False
                break
    return is_in_range


def compare_text(user_params: dict[str, str], text_data: dict[str, str]):
    if "text" not in user_params or "text" not in text_data:
        return True
    return user_params["text"].lower() in text_data["text"].lower()


@sync_to_async
def ralty_is_sutable(realty: Realty, user: TelegramUser):
    user_parameters = string_to_dict(user.search_parameters)
    if not user_parameters:
        return True
    forgein_data = get_filled_fields(realty, foregin_fields)
    integer_data = get_filled_fields(realty, integer_fields)
    text_data = get_filled_fields(realty, text_fields)
    city_id = user_parameters.pop("location__city")
    realty_city_id = realty.location.city.pk
    if not int(city_id) == realty_city_id:
        return False
    if not compare_forgein(user_parameters, forgein_data):
        return False
    if not compare_integer(user_parameters, integer_data):
        return False
    if not compare_text(user_parameters, text_data):
        return False
    return True


async def send_telegram_message(pk: int):
    bot_token = os.getenv("TELEGRAM_TOKEN")
    bot = Bot(token=bot_token)
    realty = await Realty.objects.filter(pk=pk).afirst()
    async for user in TelegramUser.objects.filter(is_subscribed=True):
        if await ralty_is_sutable(realty, user):
            keyboard = [
                [
                    InlineKeyboardButton(
                        "Перейти к обьявлению",
                        callback_data="realty_" + str(pk),
                    )
                ]
            ]
            fields = get_filled_fields(realty, search_fields)
            text = f"Получено сообщение по рассылке {realty.title}"
            photo = realty.image
            print(photo)
            if not photo:
                photo = LOGO_URL_RELATIVE
            for field in fields:
                text += f"\n{FIELDS[field]}: {fields[field]}"

            reply_markup = InlineKeyboardMarkup(keyboard)
            await bot.send_photo(
                        chat_id=user.tg_id,
                        photo=photo,
                        caption=text,
                        reply_markup=reply_markup,
                    )            


async def send_telegram_message_to_all_users(message):
    bot_token = os.getenv("TELEGRAM_TOKEN")
    bot = Bot(token=bot_token)
    async for user in TelegramUser.objects.all():
        await bot.send_message(chat_id=user.tg_id, text=message)
