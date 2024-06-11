import re

from .constants import RE_FOR_MENU_FILTER, RE_FOR_REPRESENT_CITYS


def filter_main_menu(data):
    """Сравнивает данные с регулянрным выражением.
    Callable для pattern CallbackQueryHandler"""
    input_string = str(data)
    regex_pattern = RE_FOR_MENU_FILTER
    return not bool(re.match(regex_pattern, input_string))


def filter_rep_city(data):
    """Сравнивает данные с регулянрным выражением.
    Callable для pattern CallbackQueryHandler"""
    input_string = str(data)
    regex_pattern = RE_FOR_REPRESENT_CITYS
    return not bool(re.match(regex_pattern, input_string))
