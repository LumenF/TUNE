from pprint import pprint

from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.core.handlers.wsgi import WSGIRequest
from django.db import models
from django.utils.safestring import mark_safe

from apps.abstraction.preview.image_preview import preview_zoom


class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            output.append(preview_zoom(image_url))
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))


class AbstractAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ImageField: {
            'widget': AdminImageWidget
        }
    }

    def get_queryset(self, request: WSGIRequest):
        qs = self.model._default_manager.get_queryset()
        ordering = self.get_ordering(request)
        # TODO: Проверять что пользователь имеет доступ к данным
        # И принадлежит городу, так же для админа все данные
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


def app_resort(func):
    def inner(*args, **kwargs):
        app_list = func(*args, **kwargs)

        app_sort_key = 'app_label'
        app_ordering = {
            'user': 1,
            'geography': 2,
            'parameter': 3,
            'product_conf': 4,

        }

        resorted_app_list = sorted(app_list,
                                   key=lambda x: app_ordering[x[app_sort_key]]
                                   if x[app_sort_key] in app_ordering else 1000)

        model_sort_key = 'object_name'
        model_ordering = {
            'CSVModel': 0,
            'ConfigModel': 1,
            'RegionModel': 2,
            'WordModel': 3,
            'TypeKeyModel': 4,
            'KeyModel': 5,
            'CompanyModel': 6,
            'GroupModel': 7,
            'CategoryModel': 8,
            'SubCategoryModel': 9,

            'ProductTypeModel': 10,
            'ProductManufacturerModel': 11,
            'ProductCategoryModel': 12,
            'ProductSubCategoryModel': 13,

            'SegmentBaseModel': 14,
            'SegmentationModel': 15,
            'MailingSegmentModel': 16,
            'MailingCityModel': 17,
            'MailingAllModel': 18,

        }
        for app in resorted_app_list:
            app['models'].sort(
                key=lambda x: model_ordering[x[model_sort_key]] if x[model_sort_key] in model_ordering else 1000)
        return resorted_app_list

    return inner


admin.site.get_app_list = app_resort(admin.site.get_app_list)
