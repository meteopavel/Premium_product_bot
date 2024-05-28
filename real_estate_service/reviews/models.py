from django.db import models
from django.utils.translation import gettext_lazy as _
from object.models import RealEstate
from django.conf import settings
from django.db.models.signals import pre_delete
from django.dispatch import receiver

class DeletedUser(models.Model):
    username = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.username

class Review(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    real_estate = models.ForeignKey(RealEstate, related_name='reviews', on_delete=models.CASCADE)
    text = models.TextField()
    is_moderated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.author:
            return f'Review by {self.author} for {self.real_estate}'
        else:
            return f'Review for {self.real_estate}'

@receiver(pre_delete, sender=settings.AUTH_USER_MODEL)
def set_deleted_user(sender, instance, **kwargs):
    deleted_user, _ = DeletedUser.objects.get_or_create(username="Deleted User")
    Review.objects.filter(author=instance).update(author=deleted_user)