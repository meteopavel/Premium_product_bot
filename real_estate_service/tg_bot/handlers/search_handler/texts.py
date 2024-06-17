from asgiref.sync import sync_to_async
from django.db.models import Model
from telegram.ext import ContextTypes

from object.models import BuldingType, Category, City, Condition


forgein_fields: dict[str, Model] = {
    "location__city": City,
    "category": Category,
    "condition": Condition,
    "building_type": BuldingType,
}

common_fields: dict[str, str] = {
    "area": "квадратов",
    "price": "рублей в месяц",
    "publish_date": "день(ей)",
    "text": "",
}
fields_name = {
    "location__city": "Город",
    "category": "Категория",
    "condition": "Состояние помещений",
    "building_type": "Тип здания",
    "area": "Площадь",
    "price": "Цена ",
    "publish_date": "Период публикации",
    "text": "Поиск по тексту",
}


@sync_to_async
def user_data_as_text(context: ContextTypes.DEFAULT_TYPE) -> str:
    text = "Вот:"
    for field in forgein_fields:
        if field in context.user_data:
            model = forgein_fields[field]
            field_name = fields_name[field]
            try:
                data = model.objects.filter(
                    id=int(context.user_data[field])
                ).first()
                text += f"\n{field_name}: {data}"
            except model.DoesNotExist:
                text += f"\n{field_name}: значение не найдено"
    for field in common_fields:
        if field in context.user_data:
            field_name = fields_name[field]
            data = (
                str(context.user_data[field])
                + " "
                + common_fields[field]
                + "."
            )
            text += f"\n{field_name}: " + data
    return text
