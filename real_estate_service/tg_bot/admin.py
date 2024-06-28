from django.contrib import admin

from .models import AreaIntervals, PriceIntervals, DateInterval


@admin.register(AreaIntervals)
class AreaIntervalsAdmin(admin.ModelAdmin):
    pass


@admin.register(PriceIntervals)
class PriceIntervalsAdmin(admin.ModelAdmin):
    pass


@admin.register(DateInterval)
class DateIntervalAdmin(admin.ModelAdmin):
    pass
