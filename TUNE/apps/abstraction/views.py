import datetime
from http.client import HTTPResponse

from django.shortcuts import render
from django.views.generic import TemplateView

from TUNE.settings import client, DEVELOPMENT
from apps.abstraction.service import (
    get_user_today_register,
    get_user_today_active,
    get_product_sale_count,
    get_product_sale, get_today_manager, get_today_booking,
)
from apps.apps.user.models import TgUserModel


class BaseView(TemplateView):
    template_name = 'admin/base.html'


class StatisticView(TemplateView):
    template_name = 'html/user.html'


def report(request):
    summ = get_product_sale_count()
    text = f'#Отчет {str(datetime.datetime.today())}' \
          f'\n\n-- <b>Пользователи</b>:' \
          f'\nВсего: {str(TgUserModel.objects.all().count())}' \
          f'\nАктив: {get_user_today_active()}' \
          f'\nНовые: {get_user_today_register()}' \
           f'' \
          f'\n\n-- <b>*Заявки</b>:' \
          f'\nЗаявок менеджеру: {get_today_manager()}' \
          f'\nЗаявок бронь: {get_today_booking()}' \
           f'' \
          f'\n\n-- <b>Б/У</b>:' \
          f'\nДобавлено шт: {summ["Добавлено"]}' \
          f'\nПродано шт: {summ["Остаток шт"]}' \
          f'\nОстаток шт: {summ["Сегодня шт"]}' \
           f'' \
           f'\n\n -- <b>**Продажи Б/У</b>:' \
          f'\nСегодня выручка: {summ["Сумма"]}' \
          f'\nСегодня прибыль: {summ["Прибыль"]}' \
           f'\n' \
          f'\nСумма остатка склада: {summ["Сумма остатка"]}' \
          f'\nСумма прибыли склада: {summ["Прибыль остатка"]}' \
           f'' \
           f'\n\n' \
           f'\n*Кол-во заявок не уникально.' \
           f'\n**При условии корректности сумм в товарах.'

    client.send_message(
        chat_id=572982939,
        text=text,
    )
    if not DEVELOPMENT:
        client.send_message(
            chat_id=255109025,
            text=text,
        )
    return render(request, 'html/empty.html' )
