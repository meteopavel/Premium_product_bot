from asgiref.sync import sync_to_async
from favorites.models import Favorite
from object.models import Realty
from tg_bot.handlers.search_handler.utils import dict_to_string
from user.models import TelegramUser, User


@sync_to_async
def get_realty_by_id(realty_id):
    return Realty.objects.get(id=realty_id)


@sync_to_async
def get_or_create_telegram_user(tg_id, first_name, last_name, username):
    return TelegramUser.objects.get_or_create(
        tg_id=tg_id,
        first_name=first_name,
        last_name=last_name,
        username=username,
    )


@sync_to_async
def get_all_realty():
    return list(Realty.objects.all())


@sync_to_async
def get_user_by_id(user_id):
    return TelegramUser.objects.get(tg_id=user_id)


@sync_to_async
def get_favorite_exists(user, realty):
    return user.favorites.filter(user=user, realty=realty).exists()


@sync_to_async
def get_favorites_by_user(user):
    return list(Favorite.objects.filter(user=user))


@sync_to_async
def create_favorites(user, realty):
    return Favorite.objects.create(user=user, realty=realty)


@sync_to_async
def save_search_parameters(user: TelegramUser, user_data):
    search_parameters = dict_to_string(user_data)
    user.search_parameters = search_parameters
    user.save()
    return


@sync_to_async
def get_admin_is_staff():
    return list(User.objects.filter(is_staff=True, is_active=True))


@sync_to_async
def get_admin_is_superuser():
    return list(User.objects.filter(is_superuser=True, is_active=True))
