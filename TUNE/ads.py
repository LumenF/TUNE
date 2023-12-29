import os
from pprint import pprint

import django
import requests

from TUNE.settings import TUNE_BASE_URL

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TUNE.settings")
django.setup()
from apps.apps.product.models import NewProductModel
from apps.apps.configs.geography.models import SuppProviderModel
from apps.apps.configs.parameter.models import KeyModel, SubCategoryModel

# pr = SuppProviderModel.objects.get(id=3)
# for product in product_3:
#     product.provider = pr
#     product.save()
#
# for i in products:
#     if i.params and 'Поставщик' not in i.params:
#         if i.provider:
#             i.params['Поставщик'] = i.provider.name
#             i.save()

# model = 'Watch'
# products = NewProductModel.objects.filter(title__contains=model)
#
# keys = KeyModel.objects.filter(type__name='Серия', subcategory__category__name=model)
# colors = KeyModel.objects.filter(type__name='Цвет', subcategory__category__name=model)
# memories = KeyModel.objects.filter(type__name='Память', subcategory__category__name=model)
# # sims = KeyModel.objects.filter(type__name='SIM', subcategory__category__name=model)
#
# for product in products:
#     if not product.params:
#         product.params = {
#             'Регион': '',
#             'Поставщик': product.provider.name if product.provider else ''
#         }
#     for key in keys:
#         if key.value.lower() in product.title.lower():
#             if not product.params or (product.params or 'Серия' in product.params and product.params['Серия'].lower() == key.value.lower()):
#                 product.params['Серия'] = key.value.replace(',', '')
#                 product.subcategory = key.subcategory
#
#     for color in colors:
#         if color.value.lower() in product.title.lower():
#             if not product.params or (product.params or 'Цвет' in product.params and product.params['Цвет'].lower() == color.value.lower()):
#                 product.params['Цвет'] = color.value.replace(',', '')
#
#     for memory in memories:
#         if memory.value.lower() in product.title.lower():
#             if not product.params or (product.params or 'Память' in product.params and product.params['Память'].lower() == memory.value.lower()):
#                 product.params['Память'] = memory.value.replace(',', '')
#
#     # for sim in sims:
#     #     if sim.value.lower() in product.title.lower():
#     #         if not product.params or (product.params or 'SIM' in product.params and product.params['SIM'].lower() == sim.value.lower()):
#     #             product.params['SIM'] = sim.value.replace(',', '')
#
#     product.save()

# model = 'iPhone'
# key = 'Цвет'
#
# products = NewProductModel.objects.filter(update=True).select_related()
# series = KeyModel.objects.filter(subcategory__category__name__contains=model, type__name=key).select_related()
# out = []
# for product in products:
#     param = product.params if product.params else {}
#     k = param.get('Цвет', None)
#     if k and 'Титан' in k:
#         param['Цвет'] = param['Цвет'].replace('Титановый ', '')
#         print(param)
#         product.save()
# for product in products:
#     # product.subcategory = None
#     # product.params = None
#     # product.save()
#
#     for seria in series:
#         if seria.value.lower() in product.title.lower() and product not in out:
#             if key == 'Серия':
#                 product.subcategory = seria.subcategory
#             param = product.params if product.params else {}
#             param[key] = seria.value.replace(',', '')
#             product.params = param
#
#             if 'watch' not in product.title.lower():
#                 out.append(product)
#
# for i in out:
#     print(i.title, '-->', i.params, '-->', i.subcategory)
#     if not i.subcategory:
#         raise ValueError(f'Нет подкатегории {str(i.title)}')
# for i in out:
#     try:
#         print(i.title, '||||||||', i.params)
#         i.save()
#     except:
#         print('------------', i.title, )


# products = NewProductModel.objects.all()
# subcategory = SubCategoryModel.objects.get(name='iPhone 14')
# provider = SuppProviderModel.objects.get(name='TUNE')
#
# for i in products:
#     if '14,' in i.title and 'Dual' in i.title:
#         if not i.params:
#             i.params = {}
#         i.subcategory = subcategory
#         i.provider = provider
#         i.params['Поставщик'] = 'tune'
#         i.params['Регион'] = ''
#         i.params['Серия'] = '15'
#         i.params['SIM'] = 'dual sim'
#         if '128 гб' in i.title.lower():
#             i.params['Память'] = '128 гб'
#         elif '256 гб' in i.title.lower():
#             i.params['Память'] = '256 гб'
#         elif '512 гб' in i.title.lower():
#             i.params['Память'] = '512 гб'
#         elif '1 тб' in i.title.lower():
#             i.params['Память'] = '1 тб'
#
#         if 'красный' in i.title.lower():
#             i.params['Цвет'] = 'красный'
#         elif 'розовый' in i.title.lower():
#             i.params['Цвет'] = 'розовый'
#         elif 'зеленый' in i.title.lower():
#             i.params['Цвет'] = 'зеленый'
#         elif 'черный' in i.title.lower():
#             i.params['Цвет'] = 'черный'
#         elif 'голубой' in i.title.lower():
#             i.params['Цвет'] = 'голубой'
#         elif 'желтый' in i.title.lower():
#             i.params['Цвет'] = 'желтый'
#         elif 'белый' in i.title.lower():
#             i.params['Цвет'] = 'белый'
#         elif 'синий' in i.title.lower():
#             i.params['Цвет'] = 'синий'
#         elif 'бежевый' in i.title.lower():
#             i.params['Цвет'] = 'бежевый'
#         elif 'серебристый' in i.title.lower():
#             i.params['Цвет'] = 'серебристый'
#         elif 'золотой' in i.title.lower():
#             i.params['Цвет'] = 'золотой'
#         elif 'чёрный' in i.title.lower():
#             i.params['Цвет'] = 'черный'
#         elif 'фиолетовый' in i.title.lower():
#             i.params['Цвет'] = 'фиолетовый'
#         elif 'темная ночь' in i.title.lower():
#             i.params['Цвет'] = 'черный'
#         elif 'сияющая звезда' in i.title.lower():
#             i.params['Цвет'] = 'сияющая звезда'
#         if 'Цвет' not in i.params: print(i, 'EROOR')
#         if 'Серия' not in i.params: print(i, 'EROOR')
#         if 'Память' not in i.params: print(i, 'EROOR')
#         i.save()