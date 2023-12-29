from aiogram import types
from aiogram.filters import Text, Command
from aiogram.fsm.context import FSMContext

import app.sale.kb as kb
from app.sale.state import StateSale

from conf.conf_bot import dp, text, client, api
from service.send_user import send_to_user
from service.validate import validate_keyboard


@dp.message(Text(text=text['Скидки']['Заголовок']))
@dp.message(Text(text=text['Скидки']['Назад']))
async def index_sale(
        message: types.Message,
        state: FSMContext = None,
):
    markup = await kb.kb_index()
    if not markup:
        return await client.send_message(
            chat_id=message.from_user.id,
            text=text['Б/У товары']['404'],
        )
    await client.send_message(
        chat_id=message.from_user.id,
        text=text['Скидки']['Сообщение'],
        reply_markup=markup['keyboard']
    )
    await state.update_data(v_sale=markup['values'])
    await state.set_state(StateSale.show)


@dp.message(StateSale.show)
@validate_keyboard('v_sale', text['Главное меню']['Назад'])
async def show_product(
        message: types.Message,
        state: FSMContext,
):
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
        caption=product['caption']
    )

    await send_to_user(
        message=message,
        inline_keyboard=inl_markup,
        text=product['caption'],
        images=product['images']
    )
