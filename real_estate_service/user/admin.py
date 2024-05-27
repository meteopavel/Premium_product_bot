from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.models import User

UserAdmin.fieldsets += (
    ('Extra Fields', {'fields': (
        'role', 'telegram_id', 'telegram_username',
        'telegram_firstname', 'telegram_lastname'
    )}),
)
admin.site.register(User, UserAdmin)
