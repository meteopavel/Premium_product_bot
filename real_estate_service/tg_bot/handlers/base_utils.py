from asgiref.sync import sync_to_async


from favorites.models import Favorite
from object.models import Realty, City
from tg_bot.handlers.search_handler.utils import dict_to_string
from user.models import TelegramUser, User, ArhivedTelegramUser
from reviews.models import Review


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
def save_search_parameters(
    user: TelegramUser,
    user_data=None,
    search_parameters=None
):
    if search_parameters:
        user.search_parameters = search_parameters
    else:
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


@sync_to_async
def get_country_from_city(city: City):
    return city.country.title


@sync_to_async
def save_arhive_user(user: TelegramUser, favorites: str, reviews: str):
    if not user:
        return
    arhived_user = ArhivedTelegramUser(
        tg_id=user.tg_id,
        is_blocked=user.is_blocked,
        created_at=user.created_at,
        is_subscribed=user.is_subscribed,
        search_parameters=user.search_parameters,
        favorites=favorites,
        reviews=reviews
    )
    arhived_user.save()


async def arhive_user(user_id: int):
    user = await TelegramUser.objects.filter(tg_id=user_id).afirst()
    favorites = []
    async for favoreite_realty in Favorite.objects.filter(
            user=user).values_list('realty_id', flat=True):
        favorites.append(int(favoreite_realty))
    reviews = []
    async for review in Review.objects.filter(author=user):
        reviews.append(int(review.pk))
    reviews = ','.join(map(str, reviews))
    favorites = ','.join(map(str, favorites))
    await save_arhive_user(user, favorites, reviews)


@sync_to_async
def set_user_review_author(user: TelegramUser, review_pk: int):
    review = Review.objects.filter(pk=review_pk).first()
    if review and not review.author:
        review.author = user
        review.save()
    return


async def restore_user(tg_user: TelegramUser) -> None:
    """Restore user from ArhivedTelegramUser"""
    tg_id = tg_user.tg_id
    arhived_user = await ArhivedTelegramUser.objects.filter(
        tg_id=tg_id).afirst()
    if not arhived_user:
        return
    await save_search_parameters(
        tg_user,
        search_parameters=arhived_user.search_parameters)
    favorites: list[str] = arhived_user.favorites.split(',')
    for realty_pk in favorites:
        realty = await Realty.objects.filter(pk=int(realty_pk)).afirst()
        if realty:
            await create_favorites(user=tg_user, realty=realty)
    reviews: list[str] = arhived_user.reviews.split(',')
    for review_pk in reviews:
        await set_user_review_author(tg_user, int(review_pk))
    tg_user.is_blocked = arhived_user.is_blocked
    tg_user.is_subscribed = arhived_user.is_subscribed
    tg_user.created_at = arhived_user.created_at
    await sync_to_async(tg_user.save)()
    await sync_to_async(arhived_user.delete)()
