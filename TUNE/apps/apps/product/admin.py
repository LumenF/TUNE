import csv
import datetime
import io
import urllib.request
from pprint import pprint

from django.contrib import admin
from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect
from django.urls import path
from django.http import HttpResponse
from django.utils.safestring import mark_safe

from TUNE.settings import DEBUG
from apps.abstraction.admin import AbstractAdmin
from apps.apps.configs.geography.models import CityModel
from apps.apps.product.SITE_API import get_catalog, create_new_catalog_item
from apps.apps.product.site import get_new_file
from apps.service.actual.base import Actual
from apps.service.actual.service import get_csv_file, CSVServiceNew
from apps.apps.configs.parameter.models import CSVModel
from apps.apps.logs.models import CSVLogs
from apps.apps.product.models import (
    ProductModel,
    PriceModel,
    FavoritesModel,
    NewProductModel,
    FavoritesSubcategoryModel, NewPriceSearchModel,
)


@admin.register(PriceModel)
class PriceAdmin(AbstractAdmin):
    change_list_template = "html/buttons.html"
    list_display = (
        'category',
        'region',
        'provider',
        'date_created',
        'id',
    )

    list_filter = (
        'date_created',
        'provider',
        'category__name',

    )
    autocomplete_fields = (
        'category',
        'provider',
        'region',
    )

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        try:
            last = CSVLogs.objects.filter().last()
            last = last.date_created.strftime("%d.%m.%Y %H:%M")
            extra_context['title'] = f'Цены актуализированы {str(last)}'
        except:
            extra_context['title'] = f'Логи актуализации пусты'

        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        """Url для запуска актуализации прайсов"""
        urls = super(PriceAdmin, self).get_urls()

        custom_urls = [
            path('start', self.start_actual, name='start_actual'),
            path('test', self.test_actual, name='test_actual'),
            path('get', self.get_csv, name='get_csv'),
        ]
        return custom_urls + urls

    def start_actual(self, request):
        """Запуск процесса актуализации"""

        qs = self.model._default_manager.get_queryset()
        city = qs[0].region.name
        data = []
        result = None
        for i in qs:
            result = Actual(admin=self, price=i, request=request)
            result = result.create_data()
            if isinstance(result, dict) or not result:
                return HttpResponseRedirect("./")
            data.append(result)
        _data = []
        for i in data:
            for j in i:
                _data.append(j)
        _data = [_data]
        file = get_csv_file(city)
        NewProductModel.objects.filter(update=True).update(amount='0')
        # for i in _data:
        #     csv = CSVService(city=city, data=i, file=file)
        #     csv.start()CSVServiceNew

        csv = CSVServiceNew(city=city, data=_data[0], file=file)
        csv.start()

        # NewPriceSearchModel.objects.all().delete()
        # price_search = []
        # for i in _data[0]:
        #     price_search.append(
        #         NewPriceSearchModel(
        #             city=CityModel.objects.get(name=i.city),
        #             provider=i.provider,
        #             params=i.values,
        #             amount=i.amount,
        #             markup=i.markup,
        #         )
        #     )
        # NewPriceSearchModel.objects.bulk_create(price_search)

        # TODO: Включить для отправки цены
        csv.write()
        if result:
            self.message_user(
                request,
                message='Актуализация успешно завершена!',
                level=messages.INFO
            )
        not_update = NewProductModel.objects.filter(update=False)

        for i in not_update:
            if i.amount:
                try:
                    i.amount = str(int(float(i.amount.replace(',', ''))))
                    i.save()
                except:
                    pass
        return HttpResponseRedirect("./")

    def test_actual(self, request):
        """Тестирование"""
        qs = self.model._default_manager.get_queryset()
        result = Actual(admin=self, price=qs[0], request=request)
        result = result.create_data()
        if result:
            self.message_user(
                request,
                message='Файлы корректны!',
                level=messages.INFO
            )
        return HttpResponseRedirect("./")

    def get_csv(self, request):
        """Скачать CSV"""
        catalog = get_catalog()
        if catalog:
            res = create_new_catalog_item(catalog)
            self.message_user(
                request,
                message=f'Создано {str(res)} товаров',
                level=messages.INFO
            )
            return HttpResponseRedirect("./")
        self.message_user(
            request,
            message='Возможно нет ответа от API сайта',
            level=messages.INFO
        )
        return HttpResponseRedirect("./")

    # def get_csv(self, request):
    #     """Скачать CSV"""
    #     # TODO: Сделать для любого города
    #     # csv = CSVModel.objects.get(city__name='Санкт-Петербург')
    #     # response = urllib.request.urlopen(csv.file.url)
    #     # lines = [i.decode('utf-8') for i in response.readlines()]
    #     # response = HttpResponse(lines, content_type='text/csv')
    #     # response['Content-Disposition'] = 'attachment; filename=price.csv'
    #     new_data = get_new_file()
    #
    #     # Создаем объект буфера в памяти для записи CSV данных
    #     buffer = io.StringIO()
    #
    #     # Открываем CSV writer, указывая разделитель ;
    #     csv_writer = csv.writer(buffer, delimiter=';')
    #
    #     # Записываем заголовки, включая "Price"
    #     csv_writer.writerow(["Tilda UID", "Parent UID", "Price", ])
    #
    #     # Записываем данные
    #     for row in new_data:
    #         # Проверяем, есть ли поле "Price" в текущей строке
    #         price = row.get("Price", "")
    #
    #         # Записываем данные, включая "Price", и обрамляем их кавычками
    #         csv_writer.writerow(
    #             [f'{row["Tilda UID"]}', f'{row["Parent UID"]}',
    #              f'{price}'])
    #
    #     # Устанавливаем указатель на начало буфера
    #     buffer.seek(0)
    #
    #     # Создаем HTTP response с данными из буфера
    #     response = HttpResponse(buffer.getvalue(), content_type='text/csv')
    #
    #     # Устанавливаем заголовок для скачивания файла
    #     response['Content-Disposition'] = 'attachment; filename=price.csv'
    #     return response

    def drop_csv(self, request):
        """Обнулить CSV"""
        self.message_user(
            request,
            message='CSV успешно обнулен!',
            level=messages.WARNING
        )
        return HttpResponseRedirect("./")


@admin.register(ProductModel)
class ProductAdmin(AbstractAdmin):
    list_display = (
        'name',
        'code',
        'amount',
        'date_sale',
        'get_status',
        'author',
        'id',
    )
    autocomplete_fields = (
        'state',
        'guarantee',
        'subcategory',
        'kit',
    )
    fields = [
        'image_1',
        'image_2',
        'image_3',
        'name',
        'amount_buy',
        'code',
        'state',
        'kit',
        'guarantee',
        'custom_guarantee',
        'subcategory',
        'text',
        'caption',
    ]
    list_filter = [
        'status',
        'state'
    ]
    search_fields = (
        'name',
        'code',
    )
    readonly_fields = (
        'caption',
    )
    ordering = (
        'date_sale',
    )
    actions = (
        'delete_product',
    )

    if DEBUG:
        fields.append('create')

    @admin.action(description='Статус')
    def get_status(self, obj):
        for i in obj.STATUS_CHOICES:
            if i[0] == obj.status:
                if i[0] == '0':
                    return mark_safe(f'<a style="border-bottom: 2px solid #ffe500;">{i[1]}</a>')
                if i[0] == '1':
                    return mark_safe(f'<a style="border-bottom: 2px solid #2f0;">{i[1]}</a>')
                if i[0] == 'sale':
                    return mark_safe(f'<a style="border-bottom: 2px solid #04ff00;">{i[1]}</a>')
                if i[0] == '2':
                    return mark_safe(f'<a style="border-bottom: 2px solid #ff00f7;">{i[1]}</a>')

                return mark_safe(f'<a style="border-bottom: 2px solid #0ff;">{i[1]}</a>')
        return 'Ошибка'

    def save_model(self, request, obj, form, change):
        groups = [i['name'] for i in request.user.groups.all().values('name')]
        if not change:
            obj.author = request.user
            obj.date_created = datetime.date.today()
            obj.date_updated = datetime.date.today()
        if change and 'Поставщик' in groups:
            if obj.status == '1':
                obj.status = '0'
        obj.save()

    def get_queryset(self, request: WSGIRequest):
        qs = self.model._default_manager.get_queryset()
        groups = [i['name'] for i in request.user.groups.all().values('name')]
        if 'SuperUser' in groups:
            pass
        if 'Поставщик' in groups:
            qs = qs.filter(author=request.user)
        return qs

    def add_view(self, request, form_url="", extra_context=None):
        groups = [i['name'] for i in request.user.groups.all().values('name')]
        if 'SuperUser' in groups:
            if 'status' not in self.fields:
                self.fields.append('status')

        if 'Менеджер' in groups:
            if 'status' in self.fields:
                self.fields.remove('status')

        if 'Поставщик' in groups:
            if 'status' in self.fields:
                self.fields.remove('status')
            # if 'author' in self.fields:
            #     self.fields.remove('author')
            if 'date_sale' in self.fields:
                self.fields.remove('date_sale')
        return self.changeform_view(request, None, form_url, extra_context)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        groups = [i['name'] for i in request.user.groups.all().values('name')]

        if 'SuperUser' in groups:
            if 'status' not in self.fields:
                self.fields.append('status')

        if 'Менеджер' in groups:
            if 'status' not in self.fields:
                self.fields.append('status')

        if 'Поставщик' in groups:
            if 'status' in self.fields:
                self.fields.remove('status')
            # if 'author' in self.fields:
            #     self.fields.remove('author')
            if 'date_sale' in self.fields:
                self.fields.remove('date_sale')
        return self.changeform_view(request, object_id, form_url, extra_context)

    @admin.action(description='Удалить')
    def delete_product(self, request, queryset):
        queryset.delete()
        self.message_user(
            request,
            message='Удалено!',
            level=messages.INFO
        )

    def has_delete_permission(self, request, obj=None):

        return False


@admin.register(FavoritesModel)
class FavoritesAdmin(AbstractAdmin):
    list_display = (
        'user',
        'product',
        'date_created',
    )
    search_fields = (
        'user__username',
        'user__tg_id',
        'product__name',
        'product__subcategory__name',
    )
    autocomplete_fields = (
        'user',
        'product',
    )
    list_filter = (
        'product__status',
        'product__subcategory__category__name',
        'product__subcategory__name',
    )


@admin.register(FavoritesSubcategoryModel)
class FavoritesSubcategoryAdmin(AbstractAdmin):
    list_display = (
        'user',
        'subcategory',
        'date_created',
    )
    search_fields = (
        'user__username',
        'user__tg_id',
        'subcategory__name',
        'subcategory__name',
    )
    autocomplete_fields = (
        'user',
        'subcategory',
    )
    list_filter = (
        'subcategory__category__name',
    )


@admin.register(NewProductModel)
class NewProductAdmin(AbstractAdmin):
    list_display = (
        'title',
        'amount',
        'amount_sale',
        'subcategory',
        'update',
        'params',
        'tilda_id',
        'tilda_UID',
        # 'UUID',
        'provider',
    )
    ordering = (
        '-amount',

    )
    autocomplete_fields = (
        'subcategory',

    )
    search_fields = (
        'title',
        'tilda_UID',
    )

    actions = (
        'set_true',
        'set_false',
    )

    list_filter = (
        'update',
    )

    @admin.action(description='Обновлять')
    def set_true(self, request, queryset):
        queryset.update(update=True)

    @admin.action(description='Не обновлять')
    def set_false(self, request, queryset):
        queryset.update(update=False)


@admin.register(NewPriceSearchModel)
class NewPriceSearchAdmin(AbstractAdmin):
    list_display = (
        'provider',
        'params',
        'amount',
        'markup',
    )

    search_fields = (
        'params',
    )

    list_filter = (
        'provider',
    )
