from django.contrib import admin
from django.contrib.admin import TabularInline, StackedInline
from django.db import models
from django.db.models import QuerySet

from src.abstractions.admin import AbstractAdmin, AdminImageWidget
from src.product.product_new.models import (
    NewProductParametersModel,
    NewProductModel,
    ImageNewProductModel)


class NewProductParametersAdmin(TabularInline):
    model = NewProductParametersModel
    extra = 1
    autocomplete_fields = (
        'parameter',
    )


class ImageNewProductAdmin(StackedInline):
    model = ImageNewProductModel
    extra = 1
    formfield_overrides = {
        models.ImageField: {
            'widget': AdminImageWidget
        }
    }


class BaseProductAdmin(AbstractAdmin):
    actions = (
        'set_is_moderation_true',
        'set_is_moderation_false',
        'set_is_sales_true',
        'set_is_sales_false',
        'set_is_booking_true',
        'set_is_booking_false',
    )

    @admin.action(description='✔️Отображать товар')
    def set_is_moderation_true(self, request, queryset: QuerySet):
        # queryset.update(is_moderation=True)
        for i in queryset:
            i.is_moderation = True
            i.save()

    @admin.action(description='✖️Отключить товар')
    def set_is_moderation_false(self, request, queryset):
        for i in queryset:
            i.is_moderation = False
            i.save()

    @admin.action(description='✔️Отметить продажу')
    def set_is_sales_true(self, request, queryset):
        for i in queryset:
            i.is_sales = True
            i.save()

    @admin.action(description='✖️Убрать продажу')
    def set_is_sales_false(self, request, queryset):
        for i in queryset:
            i.is_sales = False
            i.save()

    @admin.action(description='✔️Отметить бронь')
    def set_is_booking_true(self, request, queryset):
        for i in queryset:
            i.is_booking = True
            i.save()

    @admin.action(description='✖️Убрать бронь')
    def set_is_booking_false(self, request, queryset):
        for i in queryset:
            i.is_booking = False
            i.save()


@admin.register(NewProductModel)
class NewProductAdmin(BaseProductAdmin):
    inlines = [
        NewProductParametersAdmin,
        ImageNewProductAdmin,
    ]
    readonly_fields = (
        'name',
    )
    autocomplete_fields = (
        'series',
    )
    fields = (
        'name',
        'amount',
        'series',
        'text_post',
    )

    list_display = (
        'name',
        'is_moderation',
        'date_created',
        'id'
    )
    search_fields = (
        'name',
        'series__name',
        'series__device__name',
    )
    exclude = (
        'is_booking',
        'is_sales',
    )

    list_filter = (
        'is_moderation',
        'series__device__name',
    )
