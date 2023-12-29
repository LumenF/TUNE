import apps.apps.mailing.service as service

from apps.apps.mailing.models import MailingAllModel, MailingCityModel

from asgiref.sync import sync_to_async

from django.http import JsonResponse

from ninja import Router

from requests import Request


router_mail = Router(
    tags=['Рассылка'],
)


def mail_all(_id):
    res = MailingAllModel.objects.get(id=_id)
    products = [i['name'] for i in res.products.all().values('name')]
    return products


@router_mail.get(path='/all')
async def get_product_all(
        request: Request,
        mail_id: str
) -> JsonResponse:
    """
    Получить список всех товаров в рассылке всем
    """
    result = await sync_to_async(
        func=mail_all,
        thread_sensitive=True,
    )(mail_id)

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
                'msg': 'Type not found',

            },
            status=404,
        )


def mail_city(_id):
    res = MailingCityModel.objects.get(id=_id)
    products = [i['name'] for i in res.products.all().values('name')]
    return products


@router_mail.get(path='/city')
async def get_product_city(
        request: Request,
        mail_id: str
) -> JsonResponse:
    """
    Получить список всех товаров в рассылке по городу
    """
    result = await sync_to_async(
        func=mail_city,
        thread_sensitive=True,
    )(mail_id)

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
                'msg': 'Type not found',

            },
            status=404,
        )

################################################################
# СЕГМЕНТЫ

router_segmentation = Router(
    tags=['Сегментация'],
)


@router_segmentation.get(path="/getQuiz")
async def get_quiz_segmentation(
        request,
        segmentation_id: str,
) -> JsonResponse:
    """Получить все шаги сегментации"""
    quiz = await service.get_quiz(_id=segmentation_id)
    if quiz:
        return JsonResponse(
            data={
                'status': True,
                'msg': 'Quiz found',
                'data': quiz
            },
            status=200)
    elif not quiz:
        return JsonResponse(
            data={
                'status': False,
                'msg': 'Quiz not found',
            }, status=404)


@router_segmentation.get(path="/setQuizResult")
async def get_quiz_segmentation(
        request,
        segmentation_name: str,
        tg_id: str,
        quiz_id: str,
) -> JsonResponse:
    """Записать результат"""
    result = await service.set_quiz_result(
        segmentation_name=segmentation_name,
        tg_id=tg_id,
        quiz_id=quiz_id,
    )
    if result:
        return JsonResponse(
            data={
                'status': True,
                'msg': 'Quiz successfully set',
                'data': result
            },
            status=201,
        )
    elif not result:
        return JsonResponse(
            data={
                'status': False,
                'msg': 'Process fail!',
            }, status=502)