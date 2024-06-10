from django.contrib import admin

from .models import Favorite


@admin.register(Favorite)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "realty"]
    empty_value_display = "-нет данных-"
    list_filter = ["user", "realty"]
