from aiogram import types
from aiogram.filters import Text, Command
from aiogram.fsm.context import FSMContext

import app.budget.kb as kb
from app.budget.state import StateBudget

from conf.conf_bot import dp, text, client, api
from service.send_user import send_to_user
from service.validate import validate_keyboard


@dp.message(Text(text=text['Мой бюджет']['Заголовок']))
@dp.message(Text(text=text['Мой бюджет']['Назад']))
@dp.message(Command(commands=text['Главное меню']['Команда']))
async def index_budget(
        message: types.Message,
        state: FSMContext = None,
):
    markup = await kb.kb_index()

    await client.send_message(
        chat_id=message.from_user.id,
        text=text['Мой бюджет']['Сообщение'],
        reply_markup=markup['keyboard']
    )
    await state.update_data(v_budget=markup['values'])
    await state.set_state(StateBudget.dia)


@dp.message(StateBudget.dia)
@validate_keyboard('v_budget', text['Мой бюджет']['Назад'])
async def product_list_budget(
        message: types.Message,
        state: FSMContext,
):
    if message.text == text['Мой бюджет']['Назад']:
        return index_budget(
            message=message,
            state=state
        )
    min_max = message.text.replace('от ', '').replace('до ', '').split(' ')
    if len(min_max) != 2:
        return await client.send_message(
            chat_id=message.from_user.id,
            text=text['Мой бюджет']['Ошибка']
        )
    markup = await kb.get_budget(
        min_value=min_max[0],
        max_value=min_max[1],
    )
    if not markup:
        return await client.send_message(
            chat_id=message.from_user.id,
            text=text['Мой бюджет']['404'],
        )
    await client.send_message(
        chat_id=message.from_user.id,
        text=text['Мой бюджет']['Сообщение 2'],
        reply_markup=markup['keyboard']
    )
    await state.update_data(v_product=markup['values'])
    await state.set_state(StateBudget.show)



@dp.message(StateBudget.show)
@validate_keyboard('v_product', text['Мой бюджет']['Назад'])
async def product_list_budget(
        message: types.Message,
        state: FSMContext,
):
    if message.text == text['Мой бюджет']['Назад']:
        return index_budget(
            message=message,
            state=state
        )
    product = await api.get_product(
        product_name=message.text,
        tg_id=str(message.from_user.id)
    )
    if not product:
        return await client.send_message(
            chat_id=message.from_user.id,
            text=text['Б/У товары']['Продано'],
        )
    inl_markup = await kb.get_product_kb(
        is_favorite=product['is_favorite'],
        product_id=product['id'],
    )

    await send_to_user(
        message=message,
        inline_keyboard=inl_markup,
        text=product['caption'],
        images=product['images']
    )
