import copy
import csv
import json
import urllib.request
from pprint import pprint

import requests
from django.core.files.storage import default_storage

from io import BytesIO

from django.db.models import Max

from TUNE.settings import TUNE_BASE_URL
from apps.apps.configs.geography.models import CityModel
from apps.apps.configs.parameter.models import CSVModel, ConfigModel, KeyModel, SubCategoryModel
from apps.apps.product.models import NewProductModel, PriceModel
from apps.service.actual.base import Actual

from apps.service.typing import CSVDict, PriceDict, AmountDict, GroupDict


def get_csv_file(city_name) -> CSVModel:
    try:
        csv_model = CSVModel.objects.get(
            city=CityModel.objects.get(name=city_name)
        )
        return csv_model
    except:
        # TODO: Обработать если файла нет
        pass


def read_csv_from_url(url):
    response = urllib.request.urlopen(url)
    csv_data = response.read().decode('utf-8')
    csv_dict = csv.DictReader(csv_data.splitlines())
    return list(csv_dict)


class CSVServiceNew:

    def __init__(
            self,
            city: str,
            data: list[PriceDict],
            file,
            tilda_uid=None,
    ):
        self.city_name = city
        self.data = data
        self.file: CSVModel = file
        self.tilda_uid = tilda_uid
        self.products: list[dict] = list(
            NewProductModel.objects.filter(update=True).values('tilda_UID', 'title', 'params'))
        self.block_id = []
        self.colors = [i['value'] for i in KeyModel.objects.filter(type__name='Цвет').values('value')]

    @staticmethod
    def get_new_amount(amount, markup) -> str:
        price = int(amount) + int(markup)
        #
        # if price % 1000 == 0:
        #     rounded_price = int(price / 1000) * 1000 - 10
        # else:
        #     rounded_price = int(price / 500) * 500 - 10
        formatted_price = "{:,}".format(price)
        return str(formatted_price)

    def start(self):
        # eSIM только в этом списке/ проверка серии
        list_esim = ['15,', '15 plus,', '15 pro,', '15 pro max,', '14,', '14 plus,', '14 pro,', '14 pro max,',]
        for i in self.data:
            if 'SIM' in i.values and i.values['Серия'] not in list_esim and i.price.name == 'iPhone':
                i.values.pop('SIM')

        # Проверим что размер ремешка должен быть у серии
        list_size_watch = ['ultra 2,', 'ultra,']
        for i in self.data:
            if 'Размер ремешка' in i.values and i.values['Серия'] not in list_size_watch and i.price.name == 'Watch':
                i.values.pop('Размер ремешка')

        list_size_watch_2 = ['ocean']
        for i in self.data:
            if 'Размер ремешка' in i.values and i.values['Размер ремешка'] not in list_size_watch_2 and i.price.name == 'Watch':
                i.values.pop('Размер ремешка')

        # Тип ремешка
        list_type_watch = ['ultra 2,', 'ultra,']
        for i in self.data:
            if 'Тип ремешка' in i.values and i.values['Серия'] not in list_type_watch and i.price.name == 'Watch':
                i.values.pop('Тип ремешка')
        pprint(self.data)
        matching_products = []
        for i in self.data:
            if 'Поставщик' not in i.values:
                i.values['Поставщик'] = i.provider.name.lower()

        for item in self.data:
            values_to_match = {key: value.replace(',', '') for key, value in
                               item.values.items()}  # Удаляем запятые из значений
            matching_titles = []

            for product in self.products:
                params = product['params']

                # Если в values есть ключ 'SIM', то он должен быть в params, если params не None
                if 'SIM' in values_to_match and (
                        params is None or 'SIM' not in params or values_to_match['SIM'] != params.get('SIM')):
                    continue

                # Если в values нет ключа 'SIM', то в названии товара не должно быть написано 'SIM'
                if 'SIM' not in values_to_match and 'SIM' in product['title']:
                    continue

                # Проверим, содержатся ли все значения в параметрах товара, в том числе 'eSim', если он есть в params
                if params and all(
                        (value.replace(',', '') in params.values()) or (key == 'esim' and 'esim' in params) for
                        key, value in values_to_match.items()):

                    # Если в values нет ключа 'SIM', то 'eSIM' не должен быть в названии
                    if 'SIM' not in values_to_match and 'esim' in product['title'].lower():
                        continue

                    matching_titles.append({'title': product['title'], 'amount': item.amount, 'markup': item.markup,
                                            'tilda_UID': product['tilda_UID']})
            matching_products.append({'values': values_to_match, 'matching_titles': matching_titles})
        # Обновляем цены для соответствующих товаров
        for i in matching_products:
            for key, value in i.items():
                if key == 'matching_titles':
                    if value:
                        tilda_UID = value[0]['tilda_UID']
                        p = NewProductModel.objects.filter(tilda_UID=tilda_UID)
                        if p[0].amount == '0' or (int(float(p[0].amount.replace(',', '')))) < int(
                                self.get_new_amount(value[0]['amount'], value[0]['markup']).replace(',', '')):
                            p.update(amount=self.get_new_amount(value[0]['amount'], value[0]['markup']))

        # Находим максимальные цены для товаров с eSIM в каждой подгруппе
        max_prices_with_esim = (
            NewProductModel.objects.filter(amount__gt='0', params__SIM='esim')
            .values('params__Серия', 'params__Память', 'params__Поставщик')  # Учтем различия в памяти
            .annotate(max_price=Max('amount'))
        )

        # Обновляем цены для товаров с eSIM
        for max_price_info in max_prices_with_esim:
            max_price = max_price_info['max_price']
            series = max_price_info['params__Серия']
            memory = max_price_info['params__Память']
            provider = max_price_info['params__Поставщик']
            products_without_price = NewProductModel.objects.filter(
                params__Серия=series,
                params__SIM='esim',
                params__Поставщик=provider,
                params__Память=memory,
                amount='0')
            for product in products_without_price:
                product.amount = max_price
                product.save()

        # Находим максимальные цены для товаров без eSIM в каждой подгруппе
        max_prices_without_esim = (
            NewProductModel.objects.filter(amount__gt='0', params__SIM__isnull=True)
            .values('params__Серия', 'params__Память', 'params__Поставщик')  # Учтем различия в памяти
            .annotate(max_price=Max('amount'))
        )

        # Обновляем цены для товаров без eSIM
        for max_price_info in max_prices_without_esim:
            max_price = max_price_info['max_price']
            series = max_price_info['params__Серия']
            memory = max_price_info['params__Память']
            provider = max_price_info['params__Поставщик']
            products_without_price = NewProductModel.objects.filter(
                params__SIM__isnull=True,
                params__Серия=series,
                params__Память=memory,
                params__Поставщик=provider,
                amount='0')
            for product in products_without_price:
                product.amount = max_price
                product.save()

        # Часы
        max_prices_watch = (
            NewProductModel.objects.filter(amount__gt='0', subcategory__category__name='Watch')
            .values('params__Серия', 'params__Поставщик', 'params__Размер')
            .annotate(max_price=Max('amount'))
        )
        for max_price_info in max_prices_watch:
            max_price = max_price_info['max_price']
            series = max_price_info['params__Серия']
            size = max_price_info['params__Размер']
            provider = max_price_info['params__Поставщик']
            products_without_price = NewProductModel.objects.filter(
                params__Серия=series,
                params__Размер=size,
                params__Поставщик=provider,
                amount='0')
            for product in products_without_price:
                product.amount = max_price
                product.save()

        # iPad
        max_prices_ipad = (
            NewProductModel.objects.filter(amount__gt='0', subcategory__category__name='iPad')
            .values('params__Серия', 'params__Поставщик', 'params__SIM', 'params__Память')
            .annotate(max_price=Max('amount'))
        )
        for max_price_info in max_prices_ipad:
            max_price = max_price_info['max_price']
            series = max_price_info['params__Серия']
            size = max_price_info['params__SIM']
            memory = max_price_info['params__Память']
            provider = max_price_info['params__Поставщик']
            products_without_price = NewProductModel.objects.filter(
                params__Серия=series,
                params__SIM=size,
                params__Память=memory,
                params__Поставщик=provider,
                amount='0')
            for product in products_without_price:
                product.amount = max_price
                product.save()

    def write(self):
        data = []
        out = NewProductModel.objects.filter(update=True).select_related('provider')
        for i in out:
            if i.provider:
                data.append(
                    {
                        'product_id': str(i.tilda_UID),
                        'price': str(i.amount),
                        'supplier_id': (i.provider.SITE_ID),
                    }
                )
        # TODO: Тут отправить цены
        data = {'products': data}
        data_json = data
        res = requests.post(
            url=f'{TUNE_BASE_URL}index.php?route=api/all/post_catalog&token=A0kwh2L8KRzha3zicpT6VJYEMq47RTU7',
            json=data_json,
        )
        pprint(data)
        print(res)
        print(res.text)
