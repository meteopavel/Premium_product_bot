from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.models import User, TelegramUser


@admin.register(User)
class UserAdminModel(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Fields', {'fields': (
            'role', 'telegram_id', 'telegram_username',
            'telegram_firstname', 'telegram_lastname'
        )}),
    )


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'username'
    )

    search_fields = ('first_name', 'last_name', 'username')
