from django.db import models
from django.utils.translation import gettext_lazy as _
from object.models import RealEstate
from django.conf import settings


class Review(models.Model):
    class ReviewStatus(models.TextChoices):
        PENDING = 'P', _('Pending')
        APPROVED = 'A', _('Approved')
        REJECTED = 'R', _('Rejected')

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    real_estate = models.ForeignKey(RealEstate, related_name='reviews', on_delete=models.CASCADE)
    text = models.TextField()
    status = models.CharField(
        max_length=1,
        choices=ReviewStatus.choices,
        default=ReviewStatus.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.author:
            return f'Review by {self.author} for {self.real_estate}'
        else:
            return f'Review for {self.real_estate}'