from pprint import pprint

from asgiref.sync import sync_to_async
from django.db.models import QuerySet
from django.http import JsonResponse
from ninja import Router
from requests import Request

import apps.apps.product.service as service
from apps.apps.product.schemas import GetPriceSchema
from apps.utils.service import update_chapter

router_product = Router(
    tags=['Б/У товары'],
)


@router_product.get(path='/listType')
async def get_product_type_list(
        request: Request,
) -> JsonResponse:
    """
    Получить список всех типов

    [Планшет, Телефон, ...]
    """
    result = await sync_to_async(
        func=service.get_list_type,
        thread_sensitive=True,
    )()
    if result:
        await update_chapter(
            chapter='Б/У товары',
            button='Б/У товары',
        )
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
                'msg': 'Type not found',

            },
            status=404,
        )


@router_product.get(path='/listManufacturer')
async def get_manufacturer_list(
        request: Request,
        type_name: str
) -> JsonResponse:
    """
    Получить список всех производителей

    [Apple, Samsung, ...]
    """
    result = await sync_to_async(
        func=service.get_manufacturer_list,
        thread_sensitive=True,
    )(type_name)

    if result:
        await update_chapter(
            chapter='Б/У товары',
            button=type_name,
        )
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
                'msg': 'Manufacturer not found',

            },
            status=404,
        )


@router_product.get(path='/listSubcategory')
async def get_subcategory_list(
        request: Request,
        type_name: str,
        manufacturer_name: str,
) -> JsonResponse:
    """
    Получить список всех подкатегорий

    [iPhone 13, iPhone 14, ...]
    """
    result = await sync_to_async(
        func=service.get_series_list,
        thread_sensitive=True,
    )(type_name, manufacturer_name)

    if result:
        await update_chapter(
            chapter='Б/У товары',
            button=manufacturer_name,
        )
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
                'msg': 'Manufacturers not found',

            },
            status=404,
        )


@router_product.get(path='/listProducts')
async def get_product_list(
        request: Request,
        subcategory_name: str,
        tg_id: str
) -> JsonResponse:
    """
    Получить список всех товаров

    [iPhone 13 Pro 128..., iPhone 14 Red 256..., ...]
    """
    result = await sync_to_async(
        func=service.get_products,
        thread_sensitive=True,
    )(subcategory_name, tg_id)
    if result and 'id' not in result:
        await update_chapter(
            chapter='Б/У товары',
            button=subcategory_name,
        )
        return JsonResponse(
            data={
                'status': True,
                'data': result,
            },
            status=200,
        )
    elif result and 'id' in result:
        return JsonResponse(
            data={
                     'status': False,
                     'msg': 'Products not found, but subcategory ID exist',
                 } | result,
            status=202,
        )

    else:
        return JsonResponse(
            data={
                'status': False,
                'msg': 'Products or Subcategory not found',

            },
            status=404,
        )


@router_product.get(path='/getProduct')
async def get_product(
        request: Request,
        product_name: str,
        tg_id: str
) -> JsonResponse:
    """
    Получить список информацию о товаре

    """
    result = await sync_to_async(
        func=service.get_product,
        thread_sensitive=True,
    )(product_name, tg_id, )

    if result:
        # await update_chapter(
        #     chapter='Б/У товары',
        #     button=product_name,
        # )
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
                'msg': 'Manufacturer not found',

            },
            status=404,
        )


@router_product.get(path='/getProductByID')
async def get_product(
        request: Request,
        product_id: str,
        tg_id: str
) -> JsonResponse:
    """
    Получить список информацию о товаре

    """
    result = await sync_to_async(
        func=service.get_product_by_id,
        thread_sensitive=True,
    )(product_id, tg_id, )

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
                'msg': 'Manufacturer not found',

            },
            status=404,
        )


@router_product.get(path='/listProductsSale')
async def get_product_list_sale(
        request: Request,
) -> JsonResponse:
    """
    Получить список всех товаров

    [iPhone 13 Pro 128..., iPhone 14 Red 256..., ...]
    """
    result = await sync_to_async(
        func=service.get_products_sale,
        thread_sensitive=True,
    )()

    if result:
        await update_chapter(
            chapter='Скидка',
            button='Скидка'
        )
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
                'msg': 'Products not found',

            },
            status=404,
        )


@router_product.get(path='/listBudgetProducts')
async def get_product_list_budget(
        request: Request,
        min_value: str,
        max_value: str,
) -> JsonResponse:
    """
    Получить список всех товаров в ценовом диапазоне
    """

    result = await sync_to_async(
        func=service.get_products_budget,
        thread_sensitive=True,
    )(min_value, max_value)

    if result:
        await update_chapter(
            chapter='Диапазон цен',
            button=f'{min_value}:{max_value}'
        )
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
                'msg': 'Products not found',

            },
            status=404,
        )


@router_product.get(path='/search', )
async def search(
        request: Request,
        name: str,
        tg_id: str,
) -> JsonResponse:
    """
    Поиск
    """
    result = await sync_to_async(
        func=service.search,
        thread_sensitive=True,
    )(name, tg_id)

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
                'msg': 'Manufacturers not found',

            },
            status=404,
        )


################################################################

router_product_new = Router(
    tags=['Новые товары'],
)


@router_product_new.get(path='/listType')
async def get_product_type_list(
        request: Request,
) -> JsonResponse:
    """
    Получить список всех типов

    [Планшет, Телефон, ...]
    """
    result = await sync_to_async(
        func=service.get_list_type_new,
        thread_sensitive=True,
    )()

    if result:
        await update_chapter(
            chapter='Новые товары',
            button='Новые устройства'
        )
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
                'msg': 'Type not found',

            },
            status=404,
        )


@router_product_new.get(path='/listManufacturer')
async def get_manufacturer_list_new(
        request: Request,
        type_name: str
) -> JsonResponse:
    """
    Получить список всех производителей

    [Apple, Samsung, ...]
    """
    result = await sync_to_async(
        func=service.get_manufacturer_list_new,
        thread_sensitive=True,
    )(type_name)

    if result:
        await update_chapter(
            chapter='Новые товары',
            button=type_name
        )
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
                'msg': 'Manufacturer not found',

            },
            status=404,
        )


@router_product_new.get(path='/listSubcategory')
async def get_subcategory_list_new(
        request: Request,
        type_name: str,
        manufacturer_name: str,
) -> JsonResponse:
    """
    Получить список всех подкатегорий

    [iPhone 13, iPhone 14, ...]
    """
    result = await sync_to_async(
        func=service.get_series_list_new,
        thread_sensitive=True,
    )(type_name, manufacturer_name)

    if result:
        await update_chapter(
            chapter='Новые товары',
            button=manufacturer_name
        )
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
                'msg': 'Manufacturers not found',

            },
            status=404,
        )


@router_product_new.get(path='/getKeys')
async def get_subcategory_list_new(
        request: Request,
        subcategory__name: str,
) -> JsonResponse:
    """
    Получить список всех ключей

    [{'name': 'Серия': 'order_id': 1}, ...]
    """
    result = await sync_to_async(
        func=service.get_keys,
        thread_sensitive=True,
    )(subcategory__name)

    if result:
        await update_chapter(
            chapter='Новые товары',
            button=subcategory__name
        )
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
                'msg': 'Manufacturers not found',
            },
            status=404,
        )


@router_product_new.get(path='/listKeyValues')
async def get_key_values(
        request: Request,
        subcategory__name: str,
        key_name: str,
) -> JsonResponse:
    """
    Получить значения для ключа

    [{'name': '128': 'order_id': 1}, ...]
    """
    result = await sync_to_async(
        func=service.get_key_values,
        thread_sensitive=True,
    )(subcategory__name, key_name)
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
                'msg': 'Manufacturers not found',

            },
            status=404,
        )


@router_product_new.post(path='/getPrice', )
async def get_price(
        request: Request,
        data: GetPriceSchema,
) -> JsonResponse:
    """
    Получить прайс

    key_dict = {"Память": "128", "Серия": "14 Pro"}
    """
    result = await sync_to_async(
        func=service.get_price,
        thread_sensitive=True,
    )(data.subcategory__name, data.key_dict)

    if result:
        await update_chapter(
            chapter='Новые товары',
            button=data.subcategory__name
        )
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
                'msg': 'Manufacturers not found',

            },
            status=404,
        )

