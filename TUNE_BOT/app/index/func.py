from aiogram import types
from aiogram.filters import Text, Command
from aiogram.fsm.context import FSMContext

import app.index.kb as kb
from app.index.state import StateMail, QuizState
from app.user.func import index_user
from app.user.state import StateUser

from conf.conf_bot import dp, text, client, api
from service.send_user import send_to_user
from service.validate import validate_keyboard


@dp.message(Text(text=text['Главное меню']['Заголовок']))
@dp.message(Text(text=text['Главное меню']['Назад']))
@dp.message(Command(commands=text['Главное меню']['Команда']))
async def index_menu(
        message: types.Message,
        state: FSMContext = None,
        _text='Главное меню'
):
    if state:
        await state.clear()

    # search_kb = []
    # search_kb.append([
    #     types.InlineKeyboardButton(
    #         text="Поиск по товарам",
    #         switch_inline_query_current_chat=""
    #     )
    # ])
    # await message.answer(
    #     text="Выбирайте товар из нашего каталога, либо воспользуйтесь удобным поиском.",
    #     reply_markup=types.InlineKeyboardMarkup(inline_keyboard=search_kb)
    # )

    await client.send_message(
        chat_id=message.from_user.id,
        text=_text,
        reply_markup=await kb.kb_index()
    )


@dp.message(StateMail.show)
@validate_keyboard('mail_values', text['Б/У товары']['Меню']['Категория']['Назад'])
async def show_mail_all(
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
    )

    await send_to_user(
        message=message,
        inline_keyboard=inl_markup,
        text=product['caption'],
        images=product['images']
    )


@dp.callback_query(lambda callback: 'm_all.' in callback.data)
async def show_mail_all(
        callback: types.CallbackQuery,
        state: FSMContext = None,
):
    mail_id = callback.data.split('.')[1]
    result = await api.mail_all(mail_id)
    result.append('Главное меню')
    markup = []

    for i in result:
        markup.append([types.KeyboardButton(text=i)])

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=markup)
    await client.send_message(
        chat_id=callback.from_user.id,
        text='Вот все товары',
        reply_markup=markup,
    )
    await state.set_state(StateMail.show)
    await state.update_data(mail_values=result)


@dp.callback_query(lambda callback: 'm_city.' in callback.data)
async def show_mail_all(
        callback: types.CallbackQuery,
        state: FSMContext = None,
):
    mail_id = callback.data.split('.')[1]
    result = await api.mail_city(mail_id)
    result.append('Главное меню')
    markup = []

    for i in result:
        markup.append([types.KeyboardButton(text=i)])

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=markup)
    await client.send_message(
        chat_id=callback.from_user.id,
        text='Вот все товары',
        reply_markup=markup,
    )
    await state.set_state(StateMail.show)
    await state.update_data(mail_values=result)


################################################################
# СЕГМЕНТАЦИЯ

@dp.callback_query(lambda callback: 'segment.' in callback.data)
async def segment(
        callback: types.CallbackQuery,
        state: FSMContext,
):
    segment_id = callback.data.split('.')[1]
    data = await api.get_quiz(segment_id)
    if not data['status']:
        return await client.send_message(
            chat_id=callback.from_user.id,
            text='Произошла ошибка, пожалуйста, попробуйте позже.'
        )
    data = data['data']
    out = {}
    for step in data:
        if step['step'] not in out:
            out[step['step']] = []
        out[step['step']].append(step)

    steps = out[1]
    keyboard = await kb.get_kb([i['name'] for i in steps])
    text = list(filter(None, [i['text'] for i in steps]))[0]
    await client.send_message(
        chat_id=callback.from_user.id,
        text=text,
        reply_markup=keyboard['keyboard']
    )
    await state.update_data(step=1)
    await state.update_data(data=out)
    await state.update_data(values_validate=keyboard['values'])
    await state.set_state(QuizState.next)


@dp.message(QuizState.next)
@validate_keyboard('values_validate', '/start')
async def next_step(
        message: types.Message,
        state: FSMContext,
):
    data = await state.get_data()
    current = data[str(data['step'])]
    next_step_number = str([i['to'] for i in current if i['name'] == message.text][0])

    if next_step_number != 'None':
        next_step_data = data[next_step_number]
        keyboard = await kb.get_kb([i['name'] for i in next_step_data], q=True)
        text = list(filter(None, [i['text'] for i in next_step_data]))[0]
        await client.send_message(
            chat_id=message.from_user.id,
            text=text,
            reply_markup=keyboard['keyboard']
        )
        await state.update_data(step=next_step_number)
        await state.update_data(values_validate=keyboard['values'])
        return
    user_segment = str([i['finish__name'] for i in current if i['name'] == message.text][0])
    await api.set_quiz_result(
        segmentation_name=user_segment,
        tg_id=str(message.from_user.id),
        quiz_id=current[0]['base__id'],
    )
    await index_menu(
        message=message,
        state=state,
        _text='Спасибо за участие в опросе!'
    )


@dp.message(Text(text='Предыдущий вопрос'))
async def preview_step(
        message: types.Message,
        state: FSMContext,
):
    data = await state.get_data()
    current = data[str(data['step'])]
    next_step_number = str([i['to'] for i in current if i['name'] == message.text][0])

    if next_step_number != 'None':
        next_step_data = data[next_step_number]
        keyboard = await kb.get_kb([i['name'] for i in next_step_data], q=True)
        text = list(filter(None, [i['text'] for i in next_step_data]))[0]
        await client.send_message(
            chat_id=message.from_user.id,
            text=text,
            reply_markup=keyboard['keyboard']
        )
        await state.update_data(step=next_step_number)
        await state.update_data(values_validate=keyboard['values'])
        return
    user_segment = str([i['finish__name'] for i in current if i['name'] == message.text][0])
    await index_menu(
        message=message,
        state=state,
        _text='Спасибо за участие в опросе!'
    )




@dp.message(Text(text='Избранное ❤️'))
@dp.message(Command(commands='favorite',))
async def user_bonus(
        message: types.Message,
        state: FSMContext,
):

    res = await api.get_user_favorite(message.from_user.id)
    if not res['status']:
        return await client.send_message(
            chat_id=message.from_user.id,
            text=text['Избранное']['404']
        )

    markup = [[types.KeyboardButton(text=i)] for i in res['data']]
    markup.append([types.KeyboardButton(text=text['Главное меню']['Назад'])])
    markup = types.ReplyKeyboardMarkup(keyboard=markup, resize_keyboard=True)
    await client.send_message(
        chat_id=message.from_user.id,
        text=text['Избранное']['OK'],
        reply_markup=markup,
    )
    await state.set_state(StateUser.show)
    await state.update_data(v_products=res['data'])



@dp.message(StateUser.show)
@validate_keyboard('v_products', text['Главное меню']['Назад'])
async def supp_show(
        message: types.Message,
        state: FSMContext,
):
    if message.text == text['Главное меню']['Назад']:
        return await index_menu(
            message=message,
            state=state,
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
    inl_markup = await kb.get_product_kb_fav(
        is_favorite=product['is_favorite'],
        product_id=product['id'],
        caption=product['caption'],
    )

    await send_to_user(
        message=message,
        inline_keyboard=inl_markup,
        text=product['caption'],
        images=product['images']
    )


