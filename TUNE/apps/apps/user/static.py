from calendar import monthrange
from pprint import pprint

from django.db.models import Count

from apps.apps.configs.geography.models import CityModel
from apps.apps.logs.models import UserLogs
from datetime import datetime

from apps.apps.user.models import TgUserModel
from apps.service.names import get_name_month


def get_user_static_active(
        year: int,
        month: int,
) -> dict:
    # Получаем все записи, где год равен year, а месяц равен month
    logs = UserLogs.objects.filter(date_created__year=year, date_created__month=month)

    # Создаем словарь со всеми днями месяца month
    month_dict = {}
    days = monthrange(int(year), int(month))[1]
    for day in range(1, days + 1):
        month_dict[day] = 0

    # Создаем словарь со всеми count в каждый день что есть в UserLogs
    for log in logs:
        day = log.date_created.day
        month_dict[day] = log.count

    # Если записи за какой-то день нет в базе, поставить 0
    for day in month_dict:
        if month_dict[day] == 0:
            month_dict[day] = 0

    date = []
    values = []
    for key, value in month_dict.items():
        date.append(key)
        values.append(value)

    return {
        'date_activ': date,
        'values_activ': values,
        'title_activ': get_name_month(month) + ' ' + str(year)
    }


def get_user_static_register(
        year: int,
        month: int,
) -> dict:
    logs = TgUserModel.objects.filter(date_created__year=year, date_created__month=month)
    # Создаем словарь со всеми днями месяца month
    month_dict = {}
    days = monthrange(int(year), int(month))[1]
    for day in range(1, days + 1):
        month_dict[day] = 0

    # Создаем словарь со всеми TgUserModel в каждый день, где есть записи
    for log in logs:
        day = log.date_created.day
        month_dict[day] += 1

    # Если записи за какой-то день нет в базе, поставить 0
    for day in month_dict:
        if month_dict[day] == 0:
            month_dict[day] = 0

    # Создаем словарь с данными для отображения на странице

    # Создаем словарь с данными для дальнейшей обработки
    date = []
    values = []
    for key, value in month_dict.items():
        date.append(key)
        values.append(value)
    return {
        'date_register': date,
        'values_register': values,
        'title_register': get_name_month(month) + ' ' + str(year)
    }



def get_user_static_count_region():
    city_users_count = CityModel.objects.annotate(
        users_count=Count('tgusermodel'),
    ).values('name', 'users_count')

    cities = []
    values = []
    for i in city_users_count:
        cities.append(i['name'])
        values.append(i['users_count'])
    #
    # return {
    #     'regions_names': cities,
    #     'regions_values': values,
    # }
    return {'regions_data': city_users_count}