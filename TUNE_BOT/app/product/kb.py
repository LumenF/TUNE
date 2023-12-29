from aiogram import types

from conf.conf_bot import api
from service.kb import kb_resize
from conf.conf_bot import text


async def kb_index():
    v_list = await api.get_new_list_type()
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
    v_list = await api.get_new_list_manufacturer(
        type_name=type_name,
    )
    if not v_list:
        return False
    sorted_type_list = sorted(v_list, key=lambda x: x['order_id'])
    markup = await kb_resize(sorted_type_list)
    markup.append(
        [
            types.KeyboardButton(
                text=text['Новые']['Меню']['Тип']['Назад']
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
    v_list = await api.get_new_list_subcategory(
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
                text=text['Новые']['Меню']['Производитель']['Назад']
            )
        ]
    )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=markup)
    values = [i['name'] for i in v_list]
    return {
        'keyboard': markup,
        'values': values
    }


async def kb_key_values(
        category__name: str,
        key_name: str,
):
    v_list = await api.get_new_list_keys_values(
        subcategory__name=category__name,
        key_name=key_name
    )
    if not v_list:
        return False
    sorted_type_list = sorted(v_list, key=lambda x: x['order_id'])
    markup = await kb_resize(sorted_type_list)
    markup.append(
        [
            types.KeyboardButton(
                text=text['Новые']['Меню']['Ключ']['Назад']
            )
        ]
    )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=markup)
    values = [i['name'] for i in v_list]
    return {
        'keyboard': markup,
        'values': values
    }


async def kb_key_values_2(
        category__name: str,
        key_name: str,
        value: str
):
    v_list = await api.get_new_list_keys_values(
        subcategory__name=category__name,
        key_name=key_name
    )
    if not v_list:
        return False
    sorted_type_list = sorted(v_list, key=lambda x: x['order_id'])
    markup = await kb_resize(sorted_type_list)
    markup.append(
        [
            types.KeyboardButton(
                text=text['Новые']['Меню']['Ключ']['Назад 2']
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
):
    markup = [
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
