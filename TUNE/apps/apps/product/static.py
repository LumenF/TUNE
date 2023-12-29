import datetime
from pprint import pprint

from datetime import date, timedelta

from apps.apps.configs.product_conf.models import ProductSubCategoryModel
from apps.apps.logs.models import UserLogs, ProductLogs
from apps.apps.product.models import ProductModel, FavoritesModel
from apps.service.names import get_name_month

from django.db.models import Q, Count


def get_context_category():
    category_data = ProductSubCategoryModel.objects.all().values('id', 'name')
    return {'category_data': category_data}


def get_context_product(
        year: int,
        month: int,
        category_id: int,
):
    year = int(year)
    month = int(month)
    logs = ProductLogs.objects.filter(
        Q(date_created__year=year) & Q(date_created__month=month) & Q(product__subcategory__id=category_id))
    # Получаем первый день месяца
    first_day = date(year, month, 1)

    # Получаем первый день следующего месяца
    next_month = first_day.replace(day=28) + timedelta(days=4)
    last_day = next_month - timedelta(days=next_month.day)

    # Составляем список товаров и их просмотров за каждый день
    products = {}
    for log in logs:
        if log.product_id not in products:
            products[log.product_id] = {'name': log.product.name, 'count': {}}
        products[log.product_id]['count'][log.date_created.day] = log.count

    # Создаем список словарей с названием товара, списком значений и списком дат
    result = []
    days = []
    for product_id, data in products.items():
        values = [data['count'].get(day, 0) for day in range(1, last_day.day + 1)]
        result.append({'name': data['name'], 'values': values})
        days = list(range(1, last_day.day + 1))
    if result:
        return {
            'days': days,
            'products': result,
            'title': get_name_month(month) + ' ' + str(year)
        }
    else:
        days = list(range(1, last_day.day + 1))
        result = [{
            'name': 'Ничего не найдено',
            'values': [0 for i in days]
        }]
        return {
            'days': days,
            'products': result,
            'title': get_name_month(month) + ' ' + str(year)
        }


def get_context_product_amount():
    products = ProductModel.objects.filter(status__in=['3', '4', '5', ])
    # Создаем словарь для хранения суммы стоимости товаров в каждой категории
    categories = {}
    for product in products:
        subcategory = product.subcategory
        category = subcategory.category
        if category not in categories:
            categories[category] = 0
        categories[category] += product.amount

    # Создаем список словарей для вывода результатов
    result_category = []
    for category, amount in categories.items():
        category_name = category.name
        result_category.append({'category': category_name, 'amount': amount})

    # Создаем словарь для хранения суммы стоимости товаров в каждой подкатегории
    subcategories = {}
    for product in products:
        subcategory = product.subcategory
        if subcategory not in subcategories:
            subcategories[subcategory] = 0
        subcategories[subcategory] += product.amount

    # Создаем список словарей для вывода результатов
    result_subcategory = []
    for subcategory, amount in subcategories.items():
        category = subcategory.category.name
        subcategory_name = subcategory.name
        result_subcategory.append({'category': category, 'subcategory': subcategory_name, 'amount': amount})
    # Возвращаем список словарей с результатами
    out = []

    for i in result_subcategory:
        # out[i['category']].append([i['subcategory'], i['amount']])
        create = True
        for j in out:
            if j['name'] == i['category']:
                j['values'].append([i['subcategory'], i['amount']])
                create = False
        if create:
            out.append(
                {'name': i['category'],
                 'values': [[i['subcategory'], i['amount']]]
                 }
            )

    return {
        'product_category': result_category,
        'product_subcategory': out,
    }


def get_context_product_amount_sale(
        year: int,
        month: int,
):
    year = int(year)
    month = int(month)
    products = ProductModel.objects.filter(
        Q(date_sale__year=year) & Q(date_sale__month=month))
    # Создаем словарь для хранения суммы стоимости товаров в каждой категории
    categories = {}
    for product in products:
        subcategory = product.subcategory
        category = subcategory.category
        if category not in categories:
            categories[category] = 0
        categories[category] += product.amount - product.amount_buy
    # Создаем список словарей для вывода результатов
    result_category = []
    for category, amount in categories.items():
        category_name = category.name
        result_category.append({'category': category_name, 'amount': amount})

    # Создаем словарь для хранения суммы стоимости товаров в каждой подкатегории
    subcategories = {}
    for product in products:
        subcategory = product.subcategory
        if subcategory not in subcategories:
            subcategories[subcategory] = 0
        subcategories[subcategory] += product.amount - product.amount_buy

    # Создаем список словарей для вывода результатов
    result_subcategory = []
    for subcategory, amount in subcategories.items():
        category = subcategory.category.name
        subcategory_name = subcategory.name
        result_subcategory.append({'category': category, 'subcategory': subcategory_name, 'amount': amount})
    # Возвращаем список словарей с результатами
    out = []

    for i in result_subcategory:
        # out[i['category']].append([i['subcategory'], i['amount']])
        create = True
        for j in out:
            if j['name'] == i['category']:
                j['values'].append([i['subcategory'], i['amount']])
                create = False
        if create:
            out.append(
                {'name': i['category'],
                 'values': [[i['subcategory'], i['amount']]]
                 }
            )

    return {
        'summ_product_category': result_category,
        'summ_product_subcategory': out,
        'title': get_name_month(month) + ' ' + str(year)
    }


def get_context_product_amount_not_sale():
    """Не проданные"""

    products = ProductModel.objects.filter(status__in=['0', '1', '2', 'sale'])
    # Создаем словарь для хранения суммы стоимости товаров в каждой категории
    categories = {}
    for product in products:
        subcategory = product.subcategory
        category = subcategory.category
        if category not in categories:
            categories[category] = 0
        categories[category] += product.amount - product.amount_buy

    # Создаем список словарей для вывода результатов
    result_category = []
    for category, amount in categories.items():
        category_name = category.name
        result_category.append({'category': category_name, 'amount': amount})

    # Создаем словарь для хранения суммы стоимости товаров в каждой подкатегории
    subcategories = {}
    for product in products:
        subcategory = product.subcategory
        if subcategory not in subcategories:
            subcategories[subcategory] = 0
        subcategories[subcategory] += product.amount - product.amount_buy

    # Создаем список словарей для вывода результатов
    result_subcategory = []
    for subcategory, amount in subcategories.items():
        category = subcategory.category.name
        subcategory_name = subcategory.name
        result_subcategory.append({'category': category, 'subcategory': subcategory_name, 'amount': amount})
    # Возвращаем список словарей с результатами
    out = []

    for i in result_subcategory:
        # out[i['category']].append([i['subcategory'], i['amount']])
        create = True
        for j in out:
            if j['name'] == i['category']:
                j['values'].append([i['subcategory'], i['amount']])
                create = False
        if create:
            out.append(
                {'name': i['category'],
                 'values': [[i['subcategory'], i['amount']]]
                 }
            )

    return {
        'summ_product_category_not': result_category,
        'summ_product_subcategory_not': out,
    }



def get_context_product_favorite():
    result = FavoritesModel.objects.filter(
            product__status__in=['1', '2', 'sale']
        ).values(
            'product__name'
        ).annotate(
            count=Count('id')
        )
    x = []
    for i in result:
        product = ProductLogs.objects.filter(
            product__name=i['product__name'],
            date_created=datetime.date.today(),

        )
        if product:
            x.append(product[0].count)
        else:
            x.append(0)
    out = {
        'products_name': [i['product__name'] for i in result],
        'count': [i['count'] for i in result],
        'count_view': x
    }

    return out
