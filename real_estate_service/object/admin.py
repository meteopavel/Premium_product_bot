from django.contrib import admin
from django.contrib.admin.models import LogEntry, DELETION
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied

from favorites.models import Favorite
from reviews.models import Review
from .models import (BuldingType, Category, City, Condition,
                     Contact, Country, Location, Realty, WorkSchedule)


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


class WorkScheduleInline(admin.TabularInline):
    model = WorkSchedule
    extra = 0

@admin.register(WorkSchedule)
class WorkScheduleAdmin(admin.ModelAdmin):
    list_display = ('realty', 'day_of_week', 'start_time', 'end_time')
    list_filter = ('day_of_week',)
    search_fields = ('realty__title',)
    raw_id_fields = ('realty',)

@admin.register(Realty)
class RealtyAdmin(admin.ModelAdmin):
    def delete_selected_objects(modeladmin, request, queryset):
        """
        Custom action to delete selected objects the same way as the delete button on each object's page.
        """
        if not modeladmin.has_delete_permission(request):
            raise PermissionDenied

        # Get the list of objects
        objects = queryset.all()

        # Loop through objects and delete each individually
        for obj in objects:
            obj_display = str(obj)
            obj_id = obj.id
            obj.delete()

            # Log the deletion
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(obj).pk,
                object_id=obj_id,
                object_repr=obj_display,
                action_flag=DELETION,
            )
    delete_selected_objects.short_description = "Деактивировать выбранные объявления (без удаления)"
    actions = [delete_selected_objects]
    list_filter = (
        "location__city__name",
        "location__city__country__title",
        "building_type__name",
        "condition__name",
        "category__name",
        "is_active",
    )
    list_display = ('title', 'is_active',)
    list_editable = ('is_active',)
    inlines = [ReviewInline, FavoritesInline, WorkScheduleInline]



class RealtyInline(admin.StackedInline):
    model = Realty
    extra = 0


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "city",
    )
    list_filter = (
        "city",
        "city__country",
    )
    inlines = [RealtyInline]

