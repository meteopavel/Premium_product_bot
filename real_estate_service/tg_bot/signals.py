from django.db.models.signals import post_save
from django.dispatch import receiver
from object.models import Realty
from .utils import send_message_to_subscribers


@receiver(post_save, sender=Realty)
async def new_object_created(sender, instance: Realty, created, **kwargs):
    if created:
        await send_message_to_subscribers(instance)
