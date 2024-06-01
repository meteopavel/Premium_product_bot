from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.models import User, TelegramUser
from django.contrib.auth.admin import UserAdmin
from user.models import User


@admin.register(User)
class UserAdminModel(UserAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'username'
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
