from asgiref.sync import sync_to_async
from django.db.models import QuerySet
from django.http import JsonResponse
from ninja import Router
from requests import Request

import apps.apps.user.service as service
from apps.apps.user.models import UserModel, TgUserModel
from apps.apps.user.schemas import CreateUserSchema, UpdateUserSchema

router_user = Router(
    tags=['Пользователи'],
)


async def get_users_by_tg_id(tg_id: int) -> QuerySet:
    queryset = TgUserModel.objects.filter(tg_id=tg_id)
    return await sync_to_async(list)(queryset)


@router_user.get(path='/getUser')
async def get_user(
        request: Request,
        tg_id: str,
) -> JsonResponse:
    """
    Получить пользователя
    """
    user = await sync_to_async(service.get_user, thread_sensitive=True)(tg_id)

    if user:
        return JsonResponse(
            data={
                'status': True,
                'data': user,
            },
            status=200,
        )
    else:
        return JsonResponse(
            data={
                'status': False,
                'msg': 'User not found',

            },
            status=404,
        )


@router_user.post(path='/createUser', )
async def create_user(
        request: Request,
        data: CreateUserSchema
) -> JsonResponse:
    """
    Создать пользователя
    """
    result = await sync_to_async(service.create_user, thread_sensitive=True)(data)

    if result:
        return JsonResponse(
            data={
                'status': True,
            },
            status=200,
        )
    else:
        return JsonResponse(
            data={
                'status': False,
                'msg': 'User already exists',

            },
            status=404,
        )


@router_user.put(path='/updateUser', )
async def update_user(
        request: Request,
        data: UpdateUserSchema
) -> JsonResponse:
    """
    Создать пользователя
    """
    result = await sync_to_async(service.update_user, thread_sensitive=True)(data)

    if result:
        return JsonResponse(
            data={
                'status': True,
            },
            status=200,
        )
    else:
        return JsonResponse(
            data={
                'status': False,
                'msg': 'User not update',

            },
            status=404,
        )


@router_user.get(path='/updateUserCity', )
async def update_user_city(
        request: Request,
        tg_id: str,
        city_name: str,

) -> JsonResponse:
    """
    Установить город пользователя
    """
    result = await sync_to_async(service.update_user_city, thread_sensitive=True)(
        tg_id,
        city_name,
    )

    if result:
        return JsonResponse(
            data={
                'status': True,
            },
            status=200,
        )
    else:
        return JsonResponse(
            data={
                'status': False,
                'msg': 'User not update',

            },
            status=404,
        )


@router_user.get(path='/getCities', )
async def get_cities(
        request: Request,
) -> JsonResponse:
    """
    Получить все города
    """
    result = await sync_to_async(service.get_cities, thread_sensitive=True)()

    if result:
        return JsonResponse(
            data={
                'status': True,
                'data': result
            },
            status=200,
        )
    else:
        return JsonResponse(
            data={
                'status': False,
                'msg': 'Cities not found',

            },
            status=404,
        )
