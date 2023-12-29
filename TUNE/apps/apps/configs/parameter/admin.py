from django.contrib import admin, messages
from django.contrib.admin import TabularInline
from django.http import HttpResponseRedirect

from apps.abstraction.admin import AbstractAdmin
from apps.apps.configs.geography.models import PointsCSVModel, PointsModel
from apps.apps.configs.parameter.models import (
    KeyModel,
    TypeKeyModel,
    CSVModel,
    CompanyModel,
    GroupModel,
    CategoryModel,
    SubCategoryModel,
    RegionModel,
    ConfigModel,
    ProductOrderingModel,
)


# @admin.register(ConfigModel)
class ConfigAdmin(AbstractAdmin):
    list_display = (
        'key',
        'value',
        'type',
        'id'
    )


# @admin.register(CSVModel)
class CSVAdmin(AbstractAdmin):
    list_display = (
        'city',
        'date_updated',
    )
    autocomplete_fields = (
        'city',
    )
    actions = (
        'show_csv',
        'show_csv_only_amount',
    )

    @admin.action(description='Показать выбранный')
    def show_csv(self, request, queryset):
        if len(queryset) != 1:
            return self.message_user(
                request=request,
                message='Вы можете выбрать только 1 файл за раз',
                level=messages.INFO
            )
        return HttpResponseRedirect(f"/csv/show/{queryset[0].id}")

    @admin.action(description='Показать только товары с ценой')
    def show_csv_only_amount(self, request, queryset):
        if len(queryset) != 1:
            return self.message_user(
                request=request,
                message='Вы можете выбрать только 1 файл за раз',
                level=messages.INFO
            )
        return HttpResponseRedirect(f"/csv/show/only_amount/{queryset[0].id}")


@admin.register(TypeKeyModel)
class TypeKeyAdmin(AbstractAdmin):
    list_display = (
        'name',
        'id',
    )
    search_fields = (
        'name',
        'id',
    )


class KeyAdmin(TabularInline):
    autocomplete_fields = (
        'type',
    )
    model = KeyModel
    extra = 0
    ordering = (
        '-type',
    )


class ProductOrderingAdmin(TabularInline):
    autocomplete_fields = (
        'type',
    )

    model = ProductOrderingModel
    extra = 0


@admin.register(CompanyModel)
class CompanyAdmin(AbstractAdmin):
    list_display = (
        'name',
        'order_id',
        'id',
    )
    search_fields = (
        'name',
    )


@admin.register(GroupModel)
class GroupAdmin(AbstractAdmin):
    list_display = (
        'name',
        'order_id',
        'id',
    )
    search_fields = (
        'name',
    )


@admin.register(CategoryModel)
class CategoryAdmin(AbstractAdmin):
    list_display = (
        'name',
        'group',
        'company',

        'id',
    )
    search_fields = (
        'name',
        'company__name',
        'group__name',

    )
    autocomplete_fields = (
        'company',
        'group',
        'mask'
    )

    list_filter = (
        'company',
        'group',
    )


@admin.register(SubCategoryModel)
class SubCategoryAdmin(AbstractAdmin):
    fields = (
        'image',
        'name',
        'amount',
        'category',
        'extra_mask',
        'text',
        'amount_sale',
        'order_id',
    )
    list_display = (
        'name',
        'category',
        'order_id',
        'id',
    )
    search_fields = (
        'name',
        'category__name',
    )
    autocomplete_fields = (
        'category',
        'extra_mask',
    )
    list_filter = (
        'category__name',
    )
    inlines = [
        ProductOrderingAdmin,
        KeyAdmin,
    ]
    ordering = (
        'category',
        'order_id',
    )


@admin.register(RegionModel)
class RegionAdmin(AbstractAdmin):
    list_display = (
        'key',
        'value',
        'date_created',
        'id',
    )


# @admin.register(PointsCSVModel)
class PointsCSVAdmin(AbstractAdmin):
    pass


# @admin.register(PointsModel)
class PointsModel1(AbstractAdmin):
    list_display = (
        'name',
        'phone',
        'value',
        'buy',
        'buy_frozen',
    )

    search_fields = (
        'name',
        'phone',
    )
