from django.contrib import admin

from .models import (
    BuldingType,
    Category,
    City,
    Condition,
    Contact,
    Realty
)


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


@admin.register(Realty)
class RealtyAdmin(admin.ModelAdmin):
    pass
