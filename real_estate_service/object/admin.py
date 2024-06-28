import csv

from django.contrib import admin, messages
from django.contrib.admin.models import LogEntry, DELETION
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import path

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
    change_list_template = 'admin/object/object/change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload_file/', self.admin_site.admin_view(self.upload_file), name='object_object_upload_file'),
        ]
        return custom_urls + urls

    def upload_file(self, request):
        if request.method == 'POST' and request.FILES.get('object_file'):
            object_file = request.FILES['object_file']
            fs = FileSystemStorage()
            filename = fs.save(object_file.name, object_file)
            uploaded_file_url = fs.url(filename)
            try:
                with open(fs.path(filename), mode="r", encoding="utf-8") as file:
                    reader = csv.DictReader(file, delimiter=';')

                    with transaction.atomic():
                        for row in reader:
                            country, created = Country.objects.get_or_create(
                                title=row.get('location_country')
                            )
                            city, created = City.objects.get_or_create(
                                name=row.get("location_city"),
                                country=country,
                                district=row.get("district"),
                            )
                            location, created = Location.objects.get_or_create(
                                city=city,
                                post_index=row.get("location_post_index"),
                                street=row.get("location_street"),
                                building=row.get("location_building"),
                                floor=row.get("location_floor"),
                            )

                            category, created = Category.objects.get_or_create(
                                name=row.get("category")
                            )
                            contact, created = Contact.objects.get_or_create(
                                name=row.get("contact_name"),
                                email=row.get("contact_email"),
                                phone_number=row.get("contact_phone_number").split(",")
                            )
                            area = row.get("area")
                            price = row.get("price")
                            area = int(area) if area and area.isdigit() else None
                            price = int(price) if price and price.isdigit() else None
                            Realty.objects.get_or_create(
                                title=row.get("title"),
                                site=row.get("site"),
                                area=area,
                                price=price,
                                category=category,
                                contact=contact,
                                location=location,
                            )
                messages.success(request, f'Файл {filename} был успешно обработан.')
                return redirect('admin:object_realty_changelist')
            except Exception as e:
                messages.error(request, f'Ошибка при обработке файла {filename}: {str(e)}')
                return redirect('admin:object_realty_changelist')

        # Подготовка контекста для рендеринга шаблона
        context = {
            'cl': self.get_changelist_instance(request),
            'opts': self.model._meta,
            'app_label': self.model._meta.app_label,
        }
        return render(request, 'admin/object/object/change_list.html', context)

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
        "street",
        "building",
    )
    list_filter = (
        "city",
        "city__country",
    )
    inlines = [RealtyInline]
