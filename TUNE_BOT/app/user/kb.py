from pprint import pprint

from aiogram import types

from conf.conf_bot import api, BOT_LOGIN
from service.kb import kb_resize
from conf.conf_bot import text


async def kb_index():
    markup = [
        [types.KeyboardButton(text='Изменить имя'), types.KeyboardButton(text='Изменить фамилию')],
        [types.KeyboardButton(text='Изменить почту'), types.KeyboardButton(text='Изменить город')],
        [types.KeyboardButton(text='Избранное ❤️'), types.KeyboardButton(text='Сотрудничество')],
        # [types.KeyboardButton(text='Избранное ❤️')],
        [types.KeyboardButton(text=text['Главное меню']['Назад'])],
    ]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=markup)
    values = [
        'Изменить имя',
        'Изменить почту',
        'Изменить фамилию',
        'Изменить город',
        'Избранное',
        'Сотрудничество',
        text['Главное меню']['Назад'],
    ]
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
