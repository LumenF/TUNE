from asgiref.sync import sync_to_async
from django.http import JsonResponse
from ninja import Router
from requests import Request

import apps.apps.product.service as service

router_favorite = Router(
    tags=['Избранное и лайки'],
)


@router_favorite.get(path='/addFavorite', )
async def add_favorite(
        request: Request,
        product_id: str,
        tg_id: str,
) -> JsonResponse:
    """
    Добавить в избранное Б/У
    """
    result = await sync_to_async(
        func=service.add_favorite,
        thread_sensitive=True,
    )(product_id, tg_id)

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
                'msg': 'Favorite already exists',

            },
            status=404,
        )


@router_favorite.get(path='/removeFavorite', )
async def remove_favorite(
        request: Request,
        product_id: str,
        tg_id: str,
) -> JsonResponse:
    """
    Удалить из избранного Б/У
    """
    result = await sync_to_async(
        func=service.remove_favorite,
        thread_sensitive=True,
    )(product_id, tg_id)

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
                'msg': 'Favorite not found',
            },
            status=404,
        )


###################################
# Категории


@router_favorite.get(path='/addFavoriteSubcategory', )
async def add_favorite_subcategory(
        request: Request,
        subcategory_id: str,
        tg_id: str,
) -> JsonResponse:
    """
    Добавить в избранное категорию Б/У
    """
    result = await sync_to_async(
        func=service.add_favorite_subcategory,
        thread_sensitive=True,
    )(subcategory_id, tg_id)

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
                'msg': 'Favorite already exists',

            },
            status=404,
        )


@router_favorite.get(path='/removeFavoriteSubcategory', )
async def remove_favorite_subcategory(
        request: Request,
        subcategory_id: str,
        tg_id: str,
) -> JsonResponse:
    """
    Удалить из избранного категорию Б/У
    """
    result = await sync_to_async(
        func=service.remove_favorite_subcategory,
        thread_sensitive=True,
    )(subcategory_id, tg_id)

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
                'msg': 'Favorite not found',
            },
            status=404,
        )


@router_favorite.get(path='/getUserFavorite', )
async def get_user_favorite(
        request: Request,
        tg_id: str,
) -> JsonResponse:
    """
    Получить список избранных товаров
    """
    result = await sync_to_async(
        func=service.get_user_favorite,
        thread_sensitive=True,
    )(tg_id)

    if result:
        return JsonResponse(
            data={
                'status': True,
                'data': result,
            },
            status=200,
        )
    else:
        return JsonResponse(
            data={
                'status': False,
                'msg': 'Favorite not found',
            },
            status=404,
        )
