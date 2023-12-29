from aiogram import types

from conf.conf_bot import text, BOT_LOGIN
from service.kb import get_resize_keyboard


async def kb_index():
    kb = [
        [
            types.KeyboardButton(text=text['Скидки']['Заголовок']),
            # types.KeyboardButton(text=''),
        ],
        [
            types.KeyboardButton(text=text['Б/У товары']['Заголовок']),
            types.KeyboardButton(text=text['Новые']['Заголовок']),
        ],
        [
            types.KeyboardButton(text=text['Trade-in']['Заголовок']),
            types.KeyboardButton(text=text['Мой бюджет']['Заголовок']),
        ],
        [
            types.KeyboardButton(text=text['Менеджер']['Заголовок']),
            types.KeyboardButton(text=text['ЛК']['Заголовок']),
        ],

    ]
    return types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=kb
    )


async def get_product_kb(
        is_favorite: bool,
        product_id: str,
):
    markup = [
        [
            types.InlineKeyboardButton(
                text='Не отслеживать' if is_favorite else 'Отслеживать',
                callback_data=f'sup.rm.{product_id}' if is_favorite else f'sup.add.{product_id}',
            ),
        ],
        [
            types.InlineKeyboardButton(
                text='Забронировать',
                callback_data=f'bitrix',
            ),
        ]
    ]
    return types.InlineKeyboardMarkup(
        inline_keyboard=markup,
    )


async def get_kb(list_value, q=None):
    keyboard = [[types.KeyboardButton(text=i)] for i in list_value]
    # if q:
    #     keyboard.append([types.KeyboardButton(text='Предыдущий вопрос')])
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                         keyboard=keyboard)

    return {
        'values': list_value,
        'keyboard': keyboard,
    }


async def get_product_kb_fav(
    is_favorite: bool,
    product_id: str,
    caption: str
):
    markup = [
        [
            types.InlineKeyboardButton(
                text='Поделиться',
                switch_inline_query=f'\n{caption}\n\n\nСсылка на товар👇👇\nhttps://t.me/{BOT_LOGIN}?start=sh_{product_id}',
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
