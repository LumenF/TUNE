import csv
import os
import urllib.request
from pprint import pprint

import django

from ads import new_out
from apps.service.actual.service import get_csv_file
from test import csv_out

# new = csv_out
# tilda = new_out
#
# from difflib import SequenceMatcher
#
#
# def get_similarity(a, b):
#     return SequenceMatcher(None, a, b).ratio()
#
# result = {}
# count = 0
# for i in tilda:
#     for j in new:
#         if j['name'].lower() in i['Title'].lower() and len(j['name'].split(' ')) > 2:
#             count += 1
#             if j['name'] not in result:
#                 result[j['name']] = {
#                     'name': j['name'],
#                     'title': i['Title'],
#                     'last_id': i['Tilda UID'],
#                     'id': j['id'],
#                 }
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TUNE.settings")
# django.setup()
#
# from apps.apps.product.models import NewProductModel
#
# for key, product in result.items():
#     tilda_UID = product.get('id')
#     last_id = product.get('last_id')
#     title = product.get('title')
#     new_product = NewProductModel.objects.get(tilda_UID=tilda_UID)
#     # Установите значение UUID из поля last_id
#     new_product.UUID = last_id
#     new_product.last_name = title
#
#     # Сохраните изменения
#     new_product.save()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TUNE.settings")
django.setup()

