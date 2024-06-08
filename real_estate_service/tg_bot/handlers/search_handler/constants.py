MAIN_MENU, CHOOSE, \
    CHOOSE_OTHER, TYPING, SAVE_CHOOSE, \
    SAVE_OTHER_CHOOSE = range(6)

RE_FOR_MENU_FILTER = r'^(other_city|menu|other_menu)$'

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
