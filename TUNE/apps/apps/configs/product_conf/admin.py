from django.contrib import admin

from apps.abstraction.admin import AbstractAdmin
from apps.apps.configs.product_conf.models import (
    ProductTypeModel,
    ProductManufacturerModel,
    ProductCategoryModel,
    ProductSubCategoryModel, ProductStateModel, ProductGuaranteeModel, ProductKitModel,
)


@admin.register(ProductTypeModel)
class ProductTypeAdmin(AbstractAdmin):
    list_display = (
        'name',
        'order_id',
        'id',
    )
    search_fields = (
        'name',
    )


@admin.register(ProductManufacturerModel)
class ProductManufacturerAdmin(AbstractAdmin):
    list_display = (
        'name',
        'order_id',
        'id',
    )
    search_fields = (
        'name',
    )
    ordering = (
        'order_id',
    )

@admin.register(ProductCategoryModel)
class ProductCategoryAdmin(AbstractAdmin):
    list_display = (
        'name',
        'type',
        'manufacturer',
        'order_id',
        'id',
    )
    search_fields = (
        'name',
    )
    autocomplete_fields = (
        'type',
        'manufacturer',
    )
    list_filter = (
        'manufacturer',
        'type',
    )


@admin.register(ProductSubCategoryModel)
class ProductSubCategoryAdmin(AbstractAdmin):
    list_display = (
        'name',
        'category',
        'order_id',
        'id',
    )
    search_fields = (
        'name',
    )
    autocomplete_fields = (
        'category',
    )
    list_filter = (
        'category__name',
    )
    ordering = (
        'category',
    )

@admin.register(ProductStateModel)
class ProductStateAdmin(AbstractAdmin):
    list_display = (
        'name',
        'id',
    )
    search_fields = (
        'name',
    )


@admin.register(ProductGuaranteeModel)
class ProductGuaranteeAdmin(AbstractAdmin):
    list_display = (
        'name',
        'id',
    )
    search_fields = (
        'name',
    )


@admin.register(ProductKitModel)
class ProductKitAdmin(AbstractAdmin):
    list_display = (
        'name',
        'category',
        'id',
    )
    search_fields = (
        'name',
    )
    autocomplete_fields = (
        'category',
    )
    list_filter = (
        'category__name',
    )
