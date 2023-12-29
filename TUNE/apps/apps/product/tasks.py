import os

import telebot
from telebot import types

from TUNE.celery_conf import app as app
from TUNE.settings import client
from apps.apps.product.models import ProductModel, FavoritesModel, FavoritesSubcategoryModel
from apps.service.sender import sender_master


@app.task()
def send_message_amount_change(
        _id: int
):
    """Уведомление о снижении цены"""
    product = ProductModel.objects.get(id=_id)
    if product.status not in ['1', 'sale']:
        return False

    users = FavoritesModel.objects.filter(
        product=product,
        user__notice=True,
    ).values('user__tg_id')

    markup = [
            [
                types.InlineKeyboardButton(
                    text='Не отслеживать',
                    callback_data=f'sup.rm.{_id}',
                ),
                types.InlineKeyboardButton(
                    text='Забронировать',
                    callback_data=f'bitrix.{_id}',
                ),
            ]
    ]
    markup = types.InlineKeyboardMarkup(
        keyboard=markup,
    )
    res = sender_master(
        client=client,
        user_list=[i['user__tg_id'] for i in users],
        text=product.caption,
        photo=product.image_1.url if product.image_1 else None,
        keyboard=markup,
        text_2='Цена на товар изменилась\n\n'
               'Вы получили это уведомление так как товар находится в избранном.'
    )

    # TODO: Логирование уведомления пользователей


@app.task()
def send_message_add_category(
        _id: int,
):
    product = ProductModel.objects.get(id=_id)
    if product.status not in ['1', 'sale']:
        return False
    users = FavoritesSubcategoryModel.objects.filter(
        subcategory=product.subcategory,
        user__notice=True,
    ).values('user__tg_id')

    markup = [
        [
            types.InlineKeyboardButton(
                text='Отслеживать товар',
                callback_data=f'sup.add.{_id}',
            ),
        ],
        [
            types.InlineKeyboardButton(
                text='Не отслеживать категорию',
                callback_data=f'sup.catrm.{product.subcategory.id}',
            ),
        ],
        [
            types.InlineKeyboardButton(
                text='Забронировать',
                callback_data=f'bitrix.{_id}',
            ),
        ]
    ]
    markup = types.InlineKeyboardMarkup(
        keyboard=markup,
    )
    res = sender_master(
        client=client,
        user_list=[i['user__tg_id'] for i in users],
        text=product.caption,
        photo=product.image_1.url,
        keyboard=markup,
        text_2='Новый товар в категории!\n\n'
               'Вы получили это уведомление так как отслеживаете категорию товара.'
    )