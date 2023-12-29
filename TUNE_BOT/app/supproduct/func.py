from aiogram import types
from aiogram.filters import Text, Command
from aiogram.fsm.context import FSMContext

import app.supproduct.kb as kb
from app.supproduct.state import StateSupp

from conf.conf_bot import dp, text, client, api
from service.send_user import send_to_user
from service.validate import validate_keyboard


@dp.message(Text(text=text['Б/У товары']['Заголовок']))
@dp.message(Text(text=text['Б/У товары']['Меню']['Тип']['Назад']))
async def index_supp(
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
        text=text['Б/У товары']['Меню']['Тип']['Сообщение'],
        reply_markup=markup['keyboard']
    )
    await state.update_data(v_types=markup['values'])
    await state.set_state(StateSupp.manufacturer)


@dp.message(StateSupp.manufacturer)
@validate_keyboard('v_types', text['Б/У товары']['Меню']['Производитель']['Назад'])
async def supp_manufacturer(
        message: types.Message,
        state: FSMContext,
):
    """
    Высылаем производителей
    :param message:
    :param state:
    :return:
    """
    if message.text == text['Б/У товары']['Меню']['Производитель']['Назад']:
        data = await state.get_data()
        msg = data['type_name']
    else:
        msg = message.text
    markup = await kb.kb_manufacturer(
        type_name=msg,
    )
    if not markup:
        return await client.send_message(
            chat_id=message.from_user.id,
            text=text['Б/У товары']['Меню']['Производитель']['404'],
        )
    await client.send_message(
        chat_id=message.from_user.id,
        text=text['Б/У товары']['Меню']['Производитель']['Сообщение'],
        reply_markup=markup['keyboard']
    )

    await state.update_data(type_name=msg)
    await state.update_data(v_manufacturer=markup['values'])
    await state.set_state(StateSupp.category)


@dp.message(StateSupp.category)
@validate_keyboard('v_manufacturer', text['Б/У товары']['Меню']['Производитель']['Назад'], text['Б/У товары']['Меню']['Категория']['Назад'])
async def supp_category(
        message: types.Message,
        state: FSMContext,
):
    """
    Высылаем производителей
    :param message:
    :param state:
    :return:
    """
    if message.text == text['Б/У товары']['Меню']['Производитель']['Назад']:
        return await supp_manufacturer(
            message=message,
            state=state,
        )
    if message.text == text['Б/У товары']['Меню']['Категория']['Назад']:
        data = await state.get_data()
        manufacturer_name = data['manufacturer_name']
        type_name = data['type_name']
    else:
        data = await state.get_data()
        manufacturer_name = message.text
        type_name = data['type_name']
    markup = await kb.kb_subcategory(
        type_name=type_name,
        manufacturer_name=manufacturer_name
    )
    if not markup:
        return await client.send_message(
            chat_id=message.from_user.id,
            text=text['Б/У товары']['Меню']['Категория']['404']
        )
    await state.update_data(manufacturer_name=manufacturer_name)
    await state.update_data(v_category=markup['values'])

    await client.send_message(
        chat_id=message.from_user.id,
        text=text['Б/У товары']['Меню']['Категория']['Сообщение'],
        reply_markup=markup['keyboard']
    )
    await state.set_state(StateSupp.subcategory)


@dp.message(StateSupp.subcategory)
@validate_keyboard('v_category', text['Б/У товары']['Меню']['Производитель']['Назад'], text['Б/У товары']['Меню']['Категория']['Назад'])
async def supp_subcategory(
        message: types.Message,
        state: FSMContext,
):
    if message.text == text['Б/У товары']['Меню']['Производитель']['Назад']:
        return await supp_category(
            message=message,
            state=state,
        )
    if message.text == text['Б/У товары']['Меню']['Категория']['Назад']:
        data = await state.get_data()
        subcategory_name = data['subcategory_name']
    else:
        subcategory_name = message.text

    markup = await kb.kb_products(
        subcategory_name=subcategory_name,
        tg_id=message.from_user.id
    )
    if not markup:
        return await client.send_message(
            chat_id=message.from_user.id,
            text=text['Б/У товары']['Меню']['Категория']['404']
        )
    if isinstance(markup, types.InlineKeyboardMarkup):
        return await client.send_message(
            chat_id=message.from_user.id,
            text=text['Б/У товары']['Меню']['Категория']['Подпишись'],
            reply_markup=markup
        )
    await state.update_data(subcategory_name=subcategory_name)
    await state.update_data(v_products=markup['values'])

    await client.send_message(
        chat_id=message.from_user.id,
        text=text['Б/У товары']['Меню']['Категория']['Сообщение'],
        reply_markup=markup['keyboard']
    )
    await state.set_state(StateSupp.show)


@dp.message(StateSupp.show)
@validate_keyboard('v_products', text['Б/У товары']['Меню']['Категория']['Назад'])
async def supp_show(
        message: types.Message,
        state: FSMContext,
):
    if message.text == text['Б/У товары']['Меню']['Категория']['Назад']:
        return await supp_category(
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
    inl_markup = await kb.get_product_kb(
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


#####
# Отслеживать

@dp.callback_query(lambda callback: 'sup.rm.' in callback.data)
async def cancel_product_favorite(
        callback: types.CallbackQuery,
        state: FSMContext = None,
):
    product_id = callback.data.split('.')[2]
    result = await api.remove_favorite(
        tg_id=callback.from_user.id,
        product_id=product_id,
    )
    if not result:
        return await client.answer_callback_query(
            callback_query_id=callback.id,
            text=text['Б/У товары']['removeFavoriteEROOR'],
            show_alert=True,
        )
    # inl_markup = await kb.get_product_kb(
    #     is_favorite=True,
    #     product_id=product_id,
    # )
    # await client.edit_message_reply_markup(
    #     chat_id=callback.from_user.id,
    #     message_id=callback.message.message_id,
    #     reply_markup=inl_markup
    # )
    await client.answer_callback_query(
        callback_query_id=callback.id,
        text=text['Б/У товары']['removeFavorite'],
        show_alert=True,
    )


@dp.callback_query(lambda callback: 'sup.add.' in callback.data)
async def cancel_product_favorite(
        callback: types.CallbackQuery,
        state: FSMContext = None,
):
    product_id = callback.data.split('.')[2]
    result = await api.add_favorite(
        tg_id=callback.from_user.id,
        product_id=product_id,
    )
    if not result:
        return await client.answer_callback_query(
            callback_query_id=callback.id,
            text=text['Б/У товары']['addFavoriteERROR'],
            show_alert=True,
        )
    # inl_markup = await kb.get_product_kb(
    #     is_favorite=False,
    #     product_id=product_id,
    # )
    # await client.edit_message_reply_markup(
    #     chat_id=callback.from_user.id,
    #     message_id=callback.message.message_id,
    #     reply_markup=inl_markup
    # )
    await client.answer_callback_query(
        callback_query_id=callback.id,
        text=text['Б/У товары']['addFavorite'],
        show_alert=True,
    )


#####
# Отслеживать категорию

@dp.callback_query(lambda callback: 'sup.catrm.' in callback.data)
async def cancel_subcategory_favorite(
        callback: types.CallbackQuery,
        state: FSMContext = None,
):
    subcategory_id = callback.data.split('.')[2]
    result = await api.remove_favorite_category(
        tg_id=callback.from_user.id,
        subcategory_id=subcategory_id,
    )
    if not result:
        return await client.answer_callback_query(
            callback_query_id=callback.id,
            text=text['Б/У товары']['removeFavoriteCategoryEROOR'],
            show_alert=True,
        )
    # inl_markup = await kb.get_product_kb(
    #     is_favorite=True,
    #     product_id=subcategory_id,
    # )
    # await client.edit_message_reply_markup(
    #     chat_id=callback.from_user.id,
    #     message_id=callback.message.message_id,
    #     reply_markup=inl_markup
    # )
    await client.answer_callback_query(
        callback_query_id=callback.id,
        text=text['Б/У товары']['removeFavorite'],
        show_alert=True,
    )


@dp.callback_query(lambda callback: 'sup.catadd.' in callback.data)
async def cancel_subcategory_favorite(
        callback: types.CallbackQuery,
        state: FSMContext = None,
):
    subcategory_id = callback.data.split('.')[2]
    result = await api.add_favorite_category(
        tg_id=callback.from_user.id,
        subcategory_id=subcategory_id,
    )
    if not result:
        return await client.answer_callback_query(
            callback_query_id=callback.id,
            text=text['Б/У товары']['addFavoriteCategoryEROOR'],
            show_alert=True,
        )
    # inl_markup = await kb.get_product_kb(
    #     is_favorite=False,
    #     product_id=subcategory_id,
    # )
    # await client.edit_message_reply_markup(
    #     chat_id=callback.from_user.id,
    #     message_id=callback.message.message_id,
    #     reply_markup=inl_markup
    # )
    await client.answer_callback_query(
        callback_query_id=callback.id,
        text=text['Б/У товары']['addFavoriteCategory'],
        show_alert=True,
    )


################################
# Забронировать

@dp.callback_query(lambda callback: 'sup.br.' in callback.data)
async def br_supp_link(
        callback: types.CallbackQuery,
        state: FSMContext = None,
):
    print(callback.data)


@dp.inline_query()
async def inline_search(inline_query: types.InlineQuery):
    res = await api.product_like(inline_query.query, str(inline_query.from_user.id))
    out = []
    count = 0

    if res:  # Добавлена проверка длины текста
        for i in res:
            out.append(
                types.InlineQueryResultArticle(
                    id=i['id'],
                    title=i['name'],
                    input_message_content=types.InputTextMessageContent(
                        message_text=f"showINL.{i['id']}"
                    ),
                    thumb_url=i['images'][0] if i['images'] else 'https://s3.timeweb.com/2481cb39-1f5a3cd1-6620-459a-860f-6d8d44288631/ico/404.jpg'
                )
            )
            count += 1
            if count == 49:
                break
    await inline_query.answer(results=out, is_personal=True)


@dp.message(lambda message: message.text.startswith('showINL'))
async def supp_show_inl(
        message: types.Message,
        state: FSMContext,
):

    product = await api.get_product_by_id(
        product_id=message.text.split('.')[1],
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
        caption=product['caption'],
    )

    await send_to_user(
        message=message,
        inline_keyboard=inl_markup,
        text=product['caption'],
        images=product['images']
    )