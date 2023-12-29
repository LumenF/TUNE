import requests
from asgiref.sync import sync_to_async
from django.db.models import QuerySet
from django.http import JsonResponse
from ninja import Router
from requests import Request

import apps.apps.product.service as service
from TUNE.settings import TUNE_BASE_URL
from apps.apps.configs.geography.models import InviteModel, PointsModel
from apps.apps.product.schemas import GetPriceSchema
from apps.apps.user.models import TgUserModel

router_invited = Router(
    tags=['Рефералы'],
)


def set_invited(url: str):
    try:
        result = InviteModel.objects.get(
            name=url,
        )
        result.increase_count()
        return {
            'image': result.image.url,
            'text': result.text,
        }
    except:
        pass


def get_bonus(
        tg_id: str,
):
    user: TgUserModel = TgUserModel.objects.filter(tg_id=tg_id).first()
    if not user:
        return False
    phone = user.phone.replace(' ', '').replace('+', '')
    url = f'{TUNE_BASE_URL}index.php?route=api/all/get_balance&token=A0kwh2L8KRzha3zicpT6VJYEMq47RTU7&phone={phone}'
    result = requests.get(url=url)
    if result.status_code == 404:
        return False

    if result.status_code == 200:
        return {
            'bonus': result.json()['balance'],
            'buy': 0,
            'buy_frozen': 0,
        }
    return {}


@router_invited.get(path='/set')
async def set_invite(
        request: Request,
        url: str,
) -> JsonResponse:
    """
    Принять реферала
    """
    result = await sync_to_async(
        func=set_invited,
        thread_sensitive=True,
    )(url)

    return JsonResponse(
        data={
            'status': True,
            'data': result
        },
        status=200,
    )


@router_invited.get(path='/bonus')
async def get_user_bonus(
        request: Request,
        tg_id: str,
) -> JsonResponse:
    """
    Получить бонусы
    """
    result = await sync_to_async(
        func=get_bonus,
        thread_sensitive=True,
    )(tg_id)

    if result:
        return JsonResponse(
            data={
                'status': True,
                'data': result
            },
            status=200,
        )
    return JsonResponse(
        data={
            'status': False,
        },
        status=404,
    )
