from django.db.models.signals import post_save
from django.dispatch import receiver
from object.models import Realty
from .utils import send_telegram_message_to_all_users
from asgiref.sync import sync_to_async


@receiver(post_save, sender=Realty)
async def new_object_created(sender, instance: Realty, created, **kwargs):
    if created:
        pk = await get_pk(instance)
        message = f'New object created: {type(pk)}'
        print(message)
        await send_telegram_message_to_all_users(message)


@sync_to_async
def get_pk(realty: Realty):
    return realty.pk
