import datetime
from random import random

from asgiref.sync import sync_to_async
from django.http import JsonResponse
from ninja import Router
from requests import Request

from apps.apps.logs.models import ManagerLogs, BookingProductLogs

router_logs = Router(
    tags=['Логи'],
)


def manager_update(tg_id):
    res = ManagerLogs.objects.filter(
        date_created=datetime.datetime.today(),
    )
    if res:
        res[0].update_count(tg_id)
    else:
        ManagerLogs.objects.create(
            date_created=datetime.datetime.today(),
            users=[tg_id]
        )


def booking_update():
    res = BookingProductLogs.objects.filter(
        date_created=datetime.datetime.today(),
    )
    if res:
        res[0].increase_count()
    else:
        BookingProductLogs.objects.create(
            date_created=datetime.datetime.today(),
        )


@router_logs.get(path='/manager')
async def press_btn_manager(
        request: Request,
        tg_id: str,
) -> JsonResponse:
    """
    Кнопка менеджер
    """
    print(tg_id)
    result = await sync_to_async(
        func=manager_update,
        thread_sensitive=True,
    )(tg_id)
    return JsonResponse(
        data={
            'status': True,
        },
        status=200,
    )


@router_logs.get(path='/booking')
async def press_btn_booking(
        request: Request,
) -> JsonResponse:
    """
    Кнопка брони
    """
    result = await sync_to_async(
        func=booking_update,
        thread_sensitive=True,
    )()
    return JsonResponse(
        data={
            'status': True,
        },
        status=200,
    )
