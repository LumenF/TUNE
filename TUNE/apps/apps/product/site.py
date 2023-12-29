import csv
import os
import urllib.request
from pprint import pprint

from apps.apps.product.models import NewProductModel
from apps.service.actual.service import get_csv_file

def get_new_file():
    products = NewProductModel.objects.all()

    file = get_csv_file('Санкт-Петербург')
    url = file.file.url

    with urllib.request.urlopen(url) as response:
        # Декодируем байты в строки и читаем CSV
        csv_data = csv.reader(response.read().decode('utf-8').splitlines(), delimiter=';')

        # Получаем заголовки (первая строка CSV файла)
        headers = next(csv_data)

        # Инициализируем список для хранения словарей
        data_list = []

        # Итерируем по строкам CSV файла
        for row in csv_data:
            # Создаем словарь для текущей строки, используя заголовки столбцов
            row_dict = {headers[i]: row[i] for i in range(len(headers))}

            # Добавляем словарь в список
            data_list.append(row_dict)
    c = 0

    stop_list = [
        'Чехол',
        'Silicone',
        'Clear Case',
        'Правый',
        'Левый',
        'Зарядный',
    ]
    # for i in products:
    #     for j in data_list:
    #         if c == 0:
    #             drop = True
    #             for s in stop_list:
    #                 if s.lower() in j['Title'].lower():
    #                     drop = False
    #             if drop:
    #                 j['Price'] = '0'
    #                 j['Price Old'] = '0'
    #         if i.amount and i.UUID:
    #             if 'Tilda UID' in j and j['Tilda UID']:
    #                 if j['Tilda UID'] == str(i.UUID):
    #                     if not i.amount:
    #                         i.amount = '0'
    #                     if (i.amount != '0' and i.amount) and i.amount_sale and str(i.amount_sale) != '0':
    #                         amount = int(str(i.amount).replace(',', '')) - int(str(i.amount_sale).replace(',', ''))
    #                         j['Price'] = str(amount)
    #                         j['Price Old'] = str(i.amount).replace(',', '')
    #                     else:
    #                         j['Price'] = str(i.amount).replace(',', '')
    #                         j['Price Old'] = '0'
    #                     continue
    #     c += 1

    for i in products:
        for j in data_list:
            if c == 0:
                drop = True
                for s in stop_list:
                    if s.lower() in j['Title'].lower():
                        drop = False
                if drop:
                    j['Price'] = '0'
                    j['Price Old'] = '0'
            if i.amount and i.tilda_id:
                if 'Tilda UID' in j and j['Tilda UID']:
                    if j['Tilda UID'] == str(i.tilda_id):
                        if not i.amount:
                            i.amount = '0'
                        if (i.amount != '0' and i.amount) and i.amount_sale and str(i.amount_sale) != '0':
                            amount = int(str(i.amount).replace(',', '')) - int(str(i.amount_sale).replace(',', ''))
                            j['Price'] = str(amount)
                            j['Price Old'] = str(i.amount).replace(',', '')
                        else:
                            j['Price'] = str(i.amount).replace(',', '')
                            j['Price Old'] = '0'
                        continue
        c += 1

    z = 0
    for i in data_list:
        if i['Price'] != 0 or i['Price'] != '0':
            z += 1
    return data_list