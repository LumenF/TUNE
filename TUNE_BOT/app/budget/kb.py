from aiogram import types

from service.kb import kb_resize
from conf.conf_bot import api, text


async def kb_index():
    markup = [
        [types.KeyboardButton(text='от 1000 до 15000'), types.KeyboardButton(text='от 15000 до 25000')],
        [types.KeyboardButton(text='от 25000 до 35000'), types.KeyboardButton(text='от 35000 до 55000')],
        [types.KeyboardButton(text='от 55000 до 75000'), types.KeyboardButton(text='от 75000 до 100000')],
        [types.KeyboardButton(text='от 100000 до 130000'), types.KeyboardButton(text='от 130000 до 200000')],
        [types.KeyboardButton(text=text['Главное меню']['Назад'])],
    ]
    values = [
        'от 1000 до 15000',
        'от 15000 до 25000',
        'от 25000 до 35000',
        'от 35000 до 55000',
        'от 55000 до 75000',
        'от 75000 до 100000',
        'от 100000 до 130000',
        'от 130000 до 200000',
    ]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=markup)
    return {
        'keyboard': markup,
        'values': values
    }


async def get_budget(
        min_value: str,
        max_value: str,
):
    v_list = await api.get_budget(
        min_value=min_value,
        max_value=max_value,
    )
    if not v_list:
        return False
    markup = [[types.KeyboardButton(text=i)] for i in v_list]
    markup.append(
        [
            types.KeyboardButton(
                text=text['Мой бюджет']['Назад']
            )
        ]
    )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=markup)
    values = [i for i in v_list]
    return {
        'keyboard': markup,
        'values': values
    }


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
        ]
    ]
    return types.InlineKeyboardMarkup(
        inline_keyboard=markup,
    )
