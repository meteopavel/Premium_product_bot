from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.models import User, TelegramUser
from django.contrib.auth.admin import UserAdmin
from user.models import User


@admin.register(User)
class UserAdminModel(UserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        ('Персональная информация', {'fields': ('first_name', 'email')}),
        ('Права', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'username',
        'created_at'
    )

    search_fields = ('first_name', 'last_name', 'username')
