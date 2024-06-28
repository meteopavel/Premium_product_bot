from user.models import ArhivedTelegramUser
from datetime import timedelta
from django.utils import timezone
from celery import shared_task
from celery.utils.log import get_task_logger

ARHIVE_DURATION = 30

logger = get_task_logger(__name__)


@shared_task
def delete_arhived_users():
    logger.info("The delete_arhived_users task just ran.")
    threshold_date = timezone.now() - timedelta(days=ARHIVE_DURATION)
    users_to_delete = ArhivedTelegramUser.objects.filter(
        arhived_at__lte=threshold_date)
    for user in users_to_delete:
        print(user)
    users_to_delete.delete()
