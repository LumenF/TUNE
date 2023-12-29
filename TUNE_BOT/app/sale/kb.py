from aiogram import types

from service.kb import kb_resize
from conf.conf_bot import api, text, BOT_LOGIN


async def kb_index():
    v_list = await api.get_list_sale()
    if not v_list:
        return False
    sorted_type_list = sorted(v_list, key=lambda x: x['name'])
    markup = [[types.KeyboardButton(text=i['name'])] for i in sorted_type_list]
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


async def get_product_kb(
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
