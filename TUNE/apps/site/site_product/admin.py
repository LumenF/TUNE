# from django.contrib import admin
#
# from apps.abstraction.admin import AbstractAdmin
# from apps.site.site_product.models import ShopManufacturerModel, ShopTypeModel, ShopCategoryModel, ShopSubCategoryModel, \
#     ShopProductModel, ProductSizeModel, ProductMemoryModel, ProductColorModel, ShopKeyModel
#
#
# @admin.register(ShopManufacturerModel)
# class ShopManufacturerAdmin(AbstractAdmin):
#     search_fields = (
#         'name',
#     )
#
#
# @admin.register(ShopTypeModel)
# class ShopTypeAdmin(AbstractAdmin):
#     search_fields = (
#         'name',
#     )
#
#
# @admin.register(ShopCategoryModel)
# class ShopCategoryAdmin(AbstractAdmin):
#     search_fields = (
#         'name',
#     )
#     autocomplete_fields = (
#         'type',
#         'manufacturer',
#     )
#
#
# @admin.register(ShopSubCategoryModel)
# class ShopSubCategoryAdmin(AbstractAdmin):
#     search_fields = (
#         'name',
#     )
#
#
# class ShopKeyAdmin(admin.TabularInline):
#     model = ShopKeyModel
#     extra = 0
#
#
# @admin.register(ShopProductModel)
# class ShopProductAdmin(AbstractAdmin):
#     search_fields = (
#         'name',
#     )
#     inlines = (
#         ShopKeyAdmin,
#     )
#
# @admin.register(ProductColorModel)
# class ProductColorAdmin(AbstractAdmin):
#     pass
#
#
# @admin.register(ProductMemoryModel)
# class ProductMemoryAdmin(AbstractAdmin):
#     pass
#
#
# @admin.register(ProductSizeModel)
# class ProductSizeAdmin(AbstractAdmin):
#     pass
