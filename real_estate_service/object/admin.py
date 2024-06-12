from django.contrib import admin

from .models import (
    BuldingType,
    Category,
    City,
    Condition,
    Contact,
    Realty,
    Location,
    Country,
    AreaIntervals,
    PriceIntervals
)
from reviews.models import Review
from favorites.models import Favorite


@admin.register(BuldingType)
class BuildingTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
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
    list_filter = (
        'location__city__name', 'location__city__country__title', 'building_type__name',
        'condition__name', 'category__name'
    )
    inlines = [ReviewInline, FavoritesInline]


class RealtyInline(admin.TabularInline):
    model = Realty
    extra = 0


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'city',)
    list_filter = ('city', 'city__country',)
    inlines = [RealtyInline]


@admin.register(AreaIntervals)
class AreaIntervalsAdmin(admin.ModelAdmin):
    pass


@admin.register(PriceIntervals)
class PriceIntervalsAdmin(admin.ModelAdmin):
    pass
