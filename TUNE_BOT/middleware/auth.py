from functools import lru_cache
from pprint import pprint
from typing import Any, Dict, Callable, Awaitable

import requests
from aiogram import types

from app.index.kb import kb_index
from conf.conf_bot import dp, client, text, api
from service.auth import AuthService
from service.send_user import send_to_user


@lru_cache(maxsize=64)
def get_keyboard_contact():
    keyboard = [[types.KeyboardButton(text='Отправить свой контакт ☎️', request_contact=True)]]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=keyboard)
    return keyboard


@dp.update.outer_middleware()
async def auth_middleware(
        handler: Callable[[types.Update, Dict[str, Any]], Awaitable[Any]],
        event: types.Update,
        data: Dict[str, Any]
) -> Any:

    if event.callback_query:
        user = event.callback_query.from_user

    else:
        if event.inline_query:
            user = event.inline_query.from_user
        else:
            user = event.message.from_user

        try:
            if len(event.message.text.split(' ')) == 2 \
                    and 'sh' in event.message.text \
                    and '/start' in event.message.text:
                _id = event.message.text.split(' ')[1].split('_')[1]
                product = await api.get_product_by_id(
                    product_id=_id,
                    tg_id=str(event.message.from_user.id)
                )

                if not product:
                    return await client.send_message(
                        chat_id=event.message.from_user.id,
                        text=text['Б/У товары']['Продано'],
                    )
                markup = [
                    [
                        types.InlineKeyboardButton(
                            text='Забронировать',
                            callback_data=f'bitrix.{_id}',
                        ),
                        types.InlineKeyboardButton(
                            text='Отслеживать',
                            callback_data=f'sup.add.{_id}',
                        ),
                    ],

                ]
                keyboard = types.InlineKeyboardMarkup(
                    inline_keyboard=markup,
                )
                await send_to_user(
                    message=event.message,
                    inline_keyboard=keyboard,
                    text=product['caption'],
                    images=product['images']
                )
                return
            if len(event.message.text.split(' ')) == 2 and '/start' in event.message.text:
                start_data = event.message.text.split(' ')
                invited_link = start_data[1]
                result = await api.set_invited(invited_link)
                await client.send_photo(
                    chat_id=user.id,
                    caption=result['data']['text'],
                    photo=result['data']['image'],
                )
        except:
            pass
    user_auth = AuthService(user)
    result = await user_auth.get_user()
    if event.message and event.message.contact:
        create_result = await user_auth.create_user(
            phone=str(event.message.contact.phone_number),
        )
        if create_result:
            await client.send_message(
                chat_id=user.id,
                text=text['Текст']['Регистрация успешна'],
                reply_markup=await kb_index()
            )
            return
    if not result:
        return await client.send_message(
            chat_id=user.id,
            text=text['Текст']['Пройди регистрацию'],
            reply_markup=get_keyboard_contact()
        )
    else:
        if result['data']['is_ban_user']:
            return await client.send_message(
                chat_id=user.id,
                text=text['Текст']['Забанен'],
                reply_markup=types.ReplyKeyboardRemove,
            )

    return await handler(event, data)
