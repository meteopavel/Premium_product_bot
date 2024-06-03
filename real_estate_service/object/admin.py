from django.contrib import admin

from .models import (
    BuldingType,
    Category,
    City,
    Condition,
    Contact,
    Realty
)
from reviews.models import Review
from favorites.models import Favorite


@admin.register(BuldingType)
class BuildingTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass


@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    pass


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0


class FavoritesInline(admin.TabularInline):
    model = Favorite
    extra = 0


@admin.register(Realty)
class RealtyAdmin(admin.ModelAdmin):
    inlines = [ReviewInline, FavoritesInline]
