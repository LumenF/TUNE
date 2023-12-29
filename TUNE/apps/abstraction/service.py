import datetime
from pprint import pprint

from django.db.models import Q

from apps.apps.logs.models import UserLogs, ProductLogs, AmountProductLogs, ManagerLogs, BookingProductLogs
from apps.apps.product.models import ProductModel
from apps.apps.user.models import TgUserModel


def get_user_today_register():
    today = datetime.datetime.today()
    user_today_register = TgUserModel.objects.filter(date_created=today).count()
    return user_today_register


def get_user_today_active():
    today = datetime.datetime.today()
    user_today_active = UserLogs.objects.filter(
        date_created__day=today.day,
        date_created__month=today.month,
        date_created__year=today.year,
    )
    if user_today_active:
        return user_today_active[0].count
    # return user_today_active
    return '0'


def get_product_sale():
    """Продано на сумму"""

    today = datetime.datetime.today()
    result = AmountProductLogs.objects.filter(
        date_created__day=today.day,
        date_created__month=today.month,
        date_created__year=today.year,
    )

    if result:
        return result[0].amount
    # return user_today_active
    return '0'


def get_product_sale_count():
    """Продано всего"""

    today = datetime.datetime.today()
    # Проданные

    products = ProductModel.objects.filter(
        date_sale__day=today.day,
        date_sale__month=today.month,
        date_sale__year=today.year,
    )
    _count_today = len(products)

    _sum = 0
    _profit = 0
    for product in products:
        _sum += int(product.amount)
        _profit += int(product.amount) - int(product.amount_buy)

    # Остатки
    products = ProductModel.objects.filter(status__in=['0', '1', 'sale', ])

    _count_all = products.count()
    _sum_active = 0
    _profit_active = 0
    for product in products:
        _sum_active += int(product.amount)
        _profit_active += int(product.amount) - int(product.amount_buy)

    _today_add = ProductModel.objects.filter(
        date_created=today
    ).count()

    return {
        'Добавлено': str("{:,}".format(_today_add)),
        'Сегодня шт': str("{:,}".format(_count_all)),
        'Остаток шт': str("{:,}".format(_count_today)),
        'Сумма': str("{:,}".format(_sum)),
        'Прибыль': str("{:,}".format(_profit)),
        'Сумма остатка': str("{:,}".format(_sum_active)),
        'Прибыль остатка': str("{:,}".format(_profit_active)),
    }


def get_today_manager():
    today = datetime.datetime.today()
    res = ManagerLogs.objects.filter(date_created=today)
    if res:
        return res[0].count
    return '0'


def get_today_booking():
    today = datetime.datetime.today()
    res = BookingProductLogs.objects.filter(date_created=today)
    if res:
        return res[0].count
    return '0'
