# import os
# from pprint import pprint
#
# import django
#
# from data import data
# import pandas as pd
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TUNE.settings")
# django.setup()
# from apps.apps.product.models import NewProductModel, ProductModel
# from apps.apps.configs.parameter.models import KeyModel, SubCategoryModel
#
# x = []
# for item_data in data:
#     product = ProductModel(
#         amount=item_data['amount'],
#         amount_buy=item_data['amount_buy'],
#         amount_sale=item_data['amount_sale'],
#         author_id=item_data['author_id'],
#         caption=item_data['caption'],
#         city_id=item_data['city_id'],
#         code=item_data['code'],
#         create=item_data['create'],
#         custom_guarantee=item_data['custom_guarantee'],
#         date_sale=item_data['date_sale'],
#         guarantee_id=item_data['guarantee_id'],
#         image_1=item_data['image_1'],
#         image_2=item_data['image_2'],
#         image_3=item_data['image_3'],
#         name=item_data['name'],
#         state_id=item_data['state_id'],
#         status=item_data['status'],
#         subcategory_id=item_data['subcategory_id'],
#         text=item_data['text'],
#         kit_id=item_data['kit_id'],
#         guarantee=item_data.get('guarantee', None),
#     )
#     x.append(product)
# ProductModel.objects.bulk_create(x)

# def read_xlsx_to_dict(file_path, sheet_name):
#     # Чтение данных из файла XLSX
#     df = pd.read_excel(file_path, sheet_name=sheet_name)
#
#     # Преобразование DataFrame в словарь
#     data_dict = df.to_dict(orient='records')
#
#     return data_dict

# Укажите путь к вашему файлу и имя листа
# file_path = 'data.xlsx'
# sheet_name = 'Products'
#
# result_dict = read_xlsx_to_dict(file_path, sheet_name)
# out = []
# ids = []
# for i in result_dict:
#     if i['upc'] and str(i['upc']) != 'nan':
#         out.append({
#             'product_id': i['product_id'],
#             'upc': str(int(i['upc'])),
#             'name': i['name(ru-ru)'],
#         })
#         # if str(int(i['upc'])) not in ids:
#         #     ids.append(str(int(i['upc'])))
#         # else:
#         #     print(ids)
#         #     print(str(int(i['upc'])))
# # pprint(out)
# # print(len(out))
#
# result = []
# products = NewProductModel.objects.all().select_related()
# for i in products:
#     for j in out:
#         _id = str(j['product_id'])
#         if str(i.tilda_UID) == _id:
#             i.tilda_id = j['upc']
#             i.save()
