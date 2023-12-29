import re
from pprint import pprint

from aiogram import types
from aiogram.filters import Text, Command
from aiogram.fsm.context import FSMContext

import app.user.kb as kb
from app.user.state import StateUser
from app.user.typing import get_user_type

from conf.conf_bot import dp, text, client, api
from service.send_user import send_to_user
from service.validate import validate_keyboard


@dp.message(Text(text=text['ЛК']['Заголовок']))
@dp.message(Text(text=text['ЛК']['Назад']))
@dp.message(Command(commands=text['ЛК']['Команда']))
async def index_user(
        message: types.Message,
        state: FSMContext = None,
):
    user = await api.get_user(
        tg_id=message.from_user.id
    )
    if not user:
        pass
    res = await api.get_bonus(message.from_user.id)
    if res['status']:
        _text = f'Количество баллов: <b>{res["data"]["bonus"]}</b>'
    else:
        #  _text = f'Мы не нашли Вас в системе лояльности😔'
        _text = f'Количество баллов: <b>0</b>'

    user = get_user_type(user['data'])
    user_text = f'Ваши данные:' \
                f'\n\nНик: {user.username}' \
                f'\nИмя: {user.first_name}' \
                f'\nФамилия: {user.last_name}' \
                f'\n\nТелефон: {user.phone}' \
                f'\nПочта: {user.email}' \
                f'\n\nГород: {user.city}' \
                f'\n\n{_text}'

    markup = await kb.kb_index()
    await client.send_message(
        chat_id=message.from_user.id,
        text=user_text,
        reply_markup=markup['keyboard']
    )


################################
# Имя


@dp.message(Text(text='Изменить имя'))
async def change_name(
        message: types.Message,
        state: FSMContext,
):
    await client.send_message(
        chat_id=message.from_user.id,
        text='Введите новое имя',
        reply_markup=types.ReplyKeyboardRemove,
    )
    await state.set_state(StateUser.first_name)


@dp.message(StateUser.first_name)
async def change_name_update(
        message: types.Message,
        state: FSMContext,
):
    res = await api.update_user(
        tg_id=message.from_user.id,
        first_name=message.text,
    )
    if res['status']:
        await state.clear()
        await client.send_message(
            chat_id=message.from_user.id,
            text='Имя <b>успешно</b> изменено!',
        )
        return await index_user(
            message=message,
            state=state,
        )

    await client.send_message(
        chat_id=message.from_user.id,
        text='Произошла <b>ошибка</b> при изменении, попробуйте позже!',
    )
    return await index_user(
        message=message,
        state=state,
    )


################################
# Фамилия


@dp.message(Text(text='Изменить фамилию'))
async def change_last_name(
        message: types.Message,
        state: FSMContext,
):
    await client.send_message(
        chat_id=message.from_user.id,
        text='Введите новую фамилию',
        reply_markup=types.ReplyKeyboardRemove,
    )
    await state.set_state(StateUser.last_name)


@dp.message(StateUser.last_name)
async def change_last_name_update(
        message: types.Message,
        state: FSMContext,
):
    res = await api.update_user(
        tg_id=message.from_user.id,
        last_name=message.text,
    )
    if res['status']:
        await state.clear()
        await client.send_message(
            chat_id=message.from_user.id,
            text='Фамилия <b>успешно</b> изменена!',
        )
        return await index_user(
            message=message,
            state=state,
        )

    await client.send_message(
        chat_id=message.from_user.id,
        text='Произошла <b>ошибка</b> при изменении, попробуйте позже!',
    )
    return await index_user(
        message=message,
        state=state,
    )


################################
# Почта


@dp.message(Text(text='Изменить почту'))
async def change_email(
        message: types.Message,
        state: FSMContext,
):
    await client.send_message(
        chat_id=message.from_user.id,
        text='Введите новую почту',
        reply_markup=types.ReplyKeyboardRemove,
    )
    await state.set_state(StateUser.email)


@dp.message(StateUser.email)
async def change_email_update(
        message: types.Message,
        state: FSMContext,
):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", message.text):
        return await client.send_message(
            chat_id=message.from_user.id,
            text='<b>Не верный формат!</b>\n\n'
                 'Повторите ввод',
        )

    res = await api.update_user(
        tg_id=message.from_user.id,
        email=message.text,
    )
    if res['status']:
        await state.clear()
        await client.send_message(
            chat_id=message.from_user.id,
            text='Почта <b>успешно</b> изменена!',
        )
        return await index_user(
            message=message,
            state=state,
        )

    await client.send_message(
        chat_id=message.from_user.id,
        text='Произошла <b>ошибка</b> при изменении, попробуйте позже!',
    )
    return await index_user(
        message=message,
        state=state,
    )


################################
# Город


@dp.message(Text(text='Изменить город'))
async def change_city(
        message: types.Message,
        state: FSMContext,
):
    res = await api.get_cities()
    markup = [[types.KeyboardButton(text=i)] for i in res['data']]
    markup = types.ReplyKeyboardMarkup(keyboard=markup, resize_keyboard=True)
    await client.send_message(
        chat_id=message.from_user.id,
        text='Выберите город на клавиатуре',
        reply_markup=markup,
    )
    await state.update_data(v_cities=res['data'])
    await state.set_state(StateUser.city)


@dp.message(StateUser.city)
async def change_city_update(
        message: types.Message,
        state: FSMContext,
):
    data = await state.get_data()
    if message.text not in data['v_cities']:
        return await client.send_message(
            chat_id=message.from_user.id,
            text='<b>Выберите город на <b>клавиатуре</b>!</b>'
        )

    res = await api.update_user_city(
        tg_id=message.from_user.id,
        city_name=message.text,
    )
    if res['status']:
        await state.clear()
        await client.send_message(
            chat_id=message.from_user.id,
            text='Город <b>успешно</b> изменен!',
        )
        return await index_user(
            message=message,
            state=state,
        )

    await client.send_message(
        chat_id=message.from_user.id,
        text='Произошла <b>ошибка</b> при изменении, попробуйте позже!',
    )
    return await index_user(
        message=message,
        state=state,
    )


################################
# Избранное и сотрудничество


@dp.message(Text(text='Сотрудничество'))
async def company(
        message: types.Message,
        state: FSMContext,
):
    markup = [
        [
            types.InlineKeyboardButton(
                text='Сайт',
                web_app=types.WebAppInfo(url='https://tuneapp.ru')
            ),
            types.InlineKeyboardButton(
                text='Таплинк',
                web_app=types.WebAppInfo(url='https://taplink.cc/tuneapple')
            ),

        ],
    ]
    markup = types.InlineKeyboardMarkup(
        inline_keyboard=markup,
    )

    await client.send_photo(
        chat_id=message.from_user.id,
        caption='Добрый день, если Вы хотите сотрудничать с ТЮН., направьте, пожалуйста, заявку в бот.' \
                '\n\nЕсли Вы поставщик, то прикрепите:' \
                '\n1) Коммерческое предложение' \
                '\n2) Прайсы' \
                '\n3) Контакт для связи' \
                '\n\nЕсли Вы блогер:' \
                '\n1) Ссылку на профиль' \
                '\n2) Статистику профиля' \
                '\n3) Контакт для связи' \
                '\n\nПо другим вопросам:' \
                '\n1) Подробное описание предложения' \
                '\n2) Контакт для связи' \
                '\n\nБудем рады сотрудничеству 😌', \
        photo='https://s3.timeweb.com/2481cb39-1f5a3cd1-6620-459a-860f-6d8d44288631/tune/static/img/favicon.jpg',
        reply_markup=markup
    )
