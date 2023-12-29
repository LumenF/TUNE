from aiogram import types

from conf.conf_bot import api, BOT_LOGIN
from service.kb import kb_resize
from conf.conf_bot import text


async def kb_index():
    v_list = await api.get_list_type()
    if not v_list:
        return False
    sorted_type_list = sorted(v_list, key=lambda x: x['order_id'])
    markup = await kb_resize(sorted_type_list)
    markup.append(
        [
            types.KeyboardButton(
                text=text['Главное меню']['Назад']
            )
        ]
    )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=markup)
    values = [i['name'] for i in v_list]
    return {
        'keyboard': markup,
        'values': values
    }


async def kb_manufacturer(
        type_name: str,
):
    v_list = await api.get_list_manufacturer(
        type_name=type_name,
    )
    if not v_list:
        return False
    sorted_type_list = sorted(v_list, key=lambda x: x['order_id'])
    markup = await kb_resize(sorted_type_list)
    markup.append(
        [
            types.KeyboardButton(
                text=text['Б/У товары']['Меню']['Тип']['Назад']
            )
        ]
    )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=markup)
    values = [i['name'] for i in v_list]
    return {
        'keyboard': markup,
        'values': values
    }


async def kb_subcategory(
        type_name: str,
        manufacturer_name: str
):
    v_list = await api.get_list_subcategory(
        type_name=type_name,
        manufacturer_name=manufacturer_name,
    )
    if not v_list:
        return False
    sorted_type_list = sorted(v_list, key=lambda x: x['order_id'])
    markup = await kb_resize(sorted_type_list)
    markup.append(
        [
            types.KeyboardButton(
                text=text['Б/У товары']['Меню']['Производитель']['Назад']
            )
        ]
    )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=markup)
    values = [i['name'] for i in v_list]
    return {
        'keyboard': markup,
        'values': values
    }


async def kb_products(
    subcategory_name: str,
    tg_id: str
):
    v_list = await api.get_list_products(
        subcategory_name=subcategory_name,
        tg_id=tg_id
    )
    if not v_list:
        return False
    if isinstance(v_list, dict):
        if v_list['checked']:
            markup = [
                [
                    types.InlineKeyboardButton(
                        text='Отписаться',
                        callback_data=f'sup.catrm.{v_list["id"]}',
                    ),
                ],

            ]
        else:
            markup = [
                [
                    types.InlineKeyboardButton(
                        text='Подписаться',
                        callback_data=f'sup.catadd.{v_list["id"]}',
                    ),
                ],

            ]
        return types.InlineKeyboardMarkup(
            inline_keyboard=markup,
        )
    sorted_type_list = sorted(v_list, key=lambda x: x['amount'])
    markup = [[types.KeyboardButton(text=i['name'])] for i in sorted_type_list]
    markup.append(
        [
            types.KeyboardButton(
                text=text['Б/У товары']['Меню']['Категория']['Назад']
            )
        ]
    )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=markup)
    values = [i['name'] for i in v_list]
    return {
        'keyboard': markup,
        'values': values
    }


async def get_product_kb(
    is_favorite: bool,
    product_id: str,
    caption: str
):
    share_text = f'\n{caption}\n\n\nСсылка на товар👇👇\nhttps://t.me/{BOT_LOGIN}?start=sh_{product_id}'

    markup = [
        [
            types.InlineKeyboardButton(
                text='Поделиться',
                switch_inline_query=share_text,
            ),
            types.InlineKeyboardButton(
                text='Не отслеживать' if is_favorite else 'Отслеживать',
                callback_data=f'sup.rm.{product_id}' if is_favorite else f'sup.add.{product_id}',
            ),

        ],
        [
            types.InlineKeyboardButton(
                text='Забронировать',
                callback_data=f'bitrix.{product_id}',
            ),
        ],

    ]
    return types.InlineKeyboardMarkup(
        inline_keyboard=markup,
    )


