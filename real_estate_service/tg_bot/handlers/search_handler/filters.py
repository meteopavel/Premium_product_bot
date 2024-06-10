import re

from .constants import RE_FOR_MENU_FILTER


def filter_chose(data):
    """Сравнивает данные с регулянрным выражением.
    Callable для pattern CallbackQueryHandler"""
    input_string = str(data)
    regex_pattern = RE_FOR_MENU_FILTER
    return not bool(re.match(regex_pattern, input_string))
