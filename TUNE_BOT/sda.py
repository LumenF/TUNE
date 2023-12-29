import datetime
import json
from pprint import pprint

import requests
from aiogram import types
from aiogram.filters import Text, Command
from aiogram.fsm.context import FSMContext

from conf.conf_bot import dp, text, client, BITRIX_URL, api


async def bitrix_valid(
        message: types.Message
):
    m_dict = message.dict()

    m_dict['from'] = m_dict['from_user']
    m_dict.pop('date')
    m_dict.pop('from_user')
    m_dict['date'] = str(datetime.datetime(2023, 7, 10, 1, 48, 18, tzinfo=datetime.timezone.utc))
    out = {
        'update_id': 123,
        'message': m_dict
    }
    data = json.dumps(out)
    requests.post(BITRIX_URL, data=data)


@dp.message()
async def bitrix(
        *args, **kwargs,
):
    event: types.Update = kwargs.get('event_update')
    await api.press_btn_manager(event.message.from_user.id)

    x = event.dict()

    x['message']['from'] = x['message']['from_user']
    x['message'].pop('date')
    x['message'].pop('from_user')
    x['date'] = str(datetime.datetime(2023, 7, 10, 1, 48, 18, tzinfo=datetime.timezone.utc))
    data = json.dumps(x)
    requests.post(BITRIX_URL, data=data)

    if event.message.text == 'Связаться с менеджером':
        await client.send_message(
            chat_id=x['message']['from']['id'],
            text=text['Менеджер']['Заявка'],
        )


@dp.callback_query(lambda callback: 'bitrix' in callback.data)
async def bitrix_inl(
        callback: types.CallbackQuery,
        state: FSMContext = None,
        **kwargs
):
    await api.press_btn_booking()
    x = callback.message.dict()
    c_split = callback.data.split('.')
    if len(c_split) > 1:
        product_id = c_split[1]
        if x['text']:
            x['text'] = x['text'] + '\n\n-------------------------------' \
                                    '\n\nЗаявка на бронь/покупку' \
                                    f'\n\nID клиента {callback.from_user.id}' \
                                    f'\n\nСсылка на клиента:' \
                                    f'\nhttps://tune-bot.ru/user/tgusermodel/?q={callback.from_user.id}' \
                                    f'\n\nСсылка на товар:' \
                                    f'\nhttps://tune-bot.ru/product/productmodel/?id={product_id}'
        elif x['caption']:
            x['caption'] = x['caption'] + '\n\n-------------------------------' \
                                          '\n\nЗаявка на бронь/покупку' \
                                          f'\n\nID клиента {callback.from_user.id}' \
                                          f'\n\nСсылка на клиента:' \
                                          f'\nhttps://tune-bot.ru/user/tgusermodel/?q={callback.from_user.id}' \
                                          f'\n\nСсылка на товар:' \
                                          f'\nhttps://tune-bot.ru/product/productmodel/?id={product_id}'
    else:
        if x['text']:
            x['text'] = x['text'] + '\n\n-------------------------------' \
                                    '\n\nЗаявка на бронь/покупку' \
                                    f'\n\nID клиента {callback.from_user.id}' \
                                    f'\n\nСсылка на клинта:' \
                                    f'\nhttps://tune-bot.ru/user/tgusermodel/?q={callback.from_user.id}'
        elif x['caption']:
            x['caption'] = x['caption'] + '\n\n-------------------------------' \
                                          '\n\nЗаявка на бронь/покупку' \
                                          f'\n\nID клиента {callback.from_user.id}' \
                                          f'\n\nСсылка на клиента:' \
                                          f'\nhttps://tune-bot.ru/user/tgusermodel/?q={callback.from_user.id}'
    x['from'] = callback.from_user.dict()
    x.pop('date')
    x.pop('from_user')
    x['date'] = str(datetime.datetime(2023, 7, 10, 1, 48, 18, tzinfo=datetime.timezone.utc))
    out = {
        'update_id': 123,
        'message': x
    }
    data = json.dumps(out)
    requests.post(BITRIX_URL, data=data)
    await client.send_message(
        chat_id=callback.from_user.id,
        text=text['Менеджер']['Заявка'],
    )
