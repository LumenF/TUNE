from pprint import pprint

from aiogram import types


async def get_resize_keyboard(list_value: list):
    len_list = len(list_value)
    exit_list = []

    async def func(i):
        it = [item for item in list_value[i:i + 2]]
        return it

    for j in range(len_list // 2 + len_list % 2):
        i = j * 2
        result = await func(i)
        exit_list.append([types.KeyboardButton(text=i['name']) for i in result])
    return exit_list


async def kb_resize(v: list):
    # print(v)
    out = []

    if v[0]['order_id'] == 0:
        out.append([types.KeyboardButton(text=v[0]['name'])])
        v.remove(v[0])
    kb = await get_resize_keyboard(v)
    return out + kb
