from asgiref.sync import sync_to_async
from django.db.models.signals import post_save
from django.dispatch import receiver
from object.models import Realty

from .utils import send_telegram_message


@receiver(post_save, sender=Realty)
async def new_object_created(sender, instance: Realty, created, **kwargs):
    if created:
        pk = await get_pk(instance)
        await send_telegram_message(pk)


@sync_to_async
def get_pk(realty: Realty):
    return realty.pk
