REPRESENT, CHOOSE, CITY_TYPING, \
    CHOOSE_OTHER, TYPING, SAVE_CHOOSE, \
    SAVE_OTHER_CHOOSE, REPRESENT_CITYS = range(8)

RE_FOR_MENU_FILTER = r'^(city_typing|menu|other_menu)$'

MAIN_FIELDS = {
    'location__city': 'Изменить город',
    'category': 'Категория',
    'price': 'Цена',
    'area': 'Площадь',
}
OTHER_FIELDS = {
    'publish_date': 'Дата обновления',
    'condition': 'Состояние помещения',
    'building_type': 'Тип здания',
    'text': 'Поиск в тексте обьявления',
}

RE_FOR_REPRESENT_CITYS = r'^(page_|main_menu|city_typing)'
