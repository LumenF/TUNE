from pprint import pprint

from aiogram import types
from aiogram.filters import Text, Command
from aiogram.fsm.context import FSMContext

import app.product.kb as kb
from app.product.state import StateNew

from conf.conf_bot import dp, text, client, api
from service.send_user import send_to_user
from service.validate import validate_keyboard


@dp.message(Text(text=text['Новые']['Заголовок']))
@dp.message(Text(text=text['Новые']['Назад']))
# @dp.message(Command(commands=text['Новые']['Команда']))
async def index_new(
        message: types.Message,
        state: FSMContext = None,
):
    # await client.send_message(
    #     chat_id=message.from_user.id,
    #     text='— 2018 «TuneApple», выездной ремонт техники Apple\n\n'
    #          '— 2020 «TuneApple», открытие магазина в Санкт-Петербурге\n\n'
    #          '— 2022 «ТЮН», открытие магазина в Москве\n\n'
    #          '— 2023 «ТЮН», первый в России маркетплейс оригинальной техники\n\n'
    #          '⭐️ Встречайте, первый в России маркетплейс оригинальной техники «ТЮН»\n\n'
    #          '🥳 Еще больше новых устройств на сайте:\n'
    #          'http://new.tuneapp.ru',
    # )
    await client.send_message(
        chat_id=message.from_user.id,
        text='Данный раздел временно недоступен, свяжитесь с менеджером.',
    )
    return
    # markup = await kb.kb_index()
    # if not markup:
    #     return await client.send_message(
    #         chat_id=message.from_user.id,
    #         text=text['Б/У товары']['404'],
    #     )
    # await client.send_message(
    #     chat_id=message.from_user.id,
    #     text=text['Б/У товары']['Меню']['Тип']['Сообщение'],
    #     reply_markup=markup['keyboard']
    # )
    # await state.update_data(v_types=markup['values'])
    # await state.set_state(StateNew.manufacturer)


@dp.message(StateNew.manufacturer)
@validate_keyboard('v_types', text['Новые']['Меню']['Производитель']['Назад'])
async def new_manufacturer(
        message: types.Message,
        state: FSMContext,
):
    """
    Высылаем производителей
    :param message:
    :param state:
    :return:
    """
    if message.text == text['Новые']['Меню']['Производитель']['Назад']:
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
            text=text['Новые']['Меню']['Производитель']['404'],
        )
    await client.send_message(
        chat_id=message.from_user.id,
        text=text['Новые']['Меню']['Производитель']['Сообщение'],
        reply_markup=markup['keyboard']
    )

    await state.update_data(type_name=msg)
    await state.update_data(v_manufacturer=markup['values'])
    await state.set_state(StateNew.category)


@dp.message(StateNew.category)
@validate_keyboard('v_manufacturer',
                   text['Новые']['Меню']['Производитель']['Назад'],
                   text['Новые']['Меню']['Тип']['Назад'],
                   text['Новые']['Меню']['Ключ']['Назад'],
                   )
async def new_category(
        message: types.Message,
        state: FSMContext,
):
    """
    Высылаем производителей
    :param message:
    :param state:
    :return:
    """

    if message.text == text['Новые']['Меню']['Производитель']['Назад']:
        return await new_manufacturer(
            message=message,
            state=state,
        )
    if message.text == text['Новые']['Меню']['Тип']['Назад']:
        return await index_new(
            message=message,
            state=state,
        )
    if message.text == text['Новые']['Меню']['Ключ']['Назад']:
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
            text='Ничего не найдено',
        )
    await state.update_data(manufacturer_name=manufacturer_name)
    await state.update_data(v_category=markup['values'])
    await state.update_data(v_step=[])

    await client.send_message(
        chat_id=message.from_user.id,
        text=text['Новые']['Меню']['Категория']['Сообщение'],
        reply_markup=markup['keyboard']
    )
    await state.set_state(StateNew.keys)


@dp.message(StateNew.keys)
@validate_keyboard(value='v_category',
                   back=text['Новые']['Меню']['Ключ']['Назад'],
                   back_2=text['Новые']['Меню']['Производитель']['Назад'],
                   back_3=text['Новые']['Меню']['Ключ']['Назад 2'],
                   )
async def new_keys(
        message: types.Message,
        state: FSMContext,
):
    if message.text == text['Новые']['Меню']['Производитель']['Назад']:
        return await new_category(
            message=message,
            state=state,
        )

    if message.text == text['Новые']['Меню']['Ключ']['Назад']:
        return await new_category(
            message=message,
            state=state,
        )

    data = await state.get_data()
    if text['Новые']['Меню']['Ключ']['Назад 2'] in message.text:
        step = data['step']
        await state.update_data(step=int(step) - 2)
        step_choice = data['step_choice']
        last_step_name = data['last_step_name']
        step_choice.pop(last_step_name, None)
        await state.update_data(step_choice=step_choice)
    data = await state.get_data()

    # Ставим ключи и выбранную серию
    if message.text in data['v_category'] and message.text not in data['v_step']:
        keys_list = await api.get_new_keys(subcategory__name=message.text)
        if not keys_list:
            # Пробуем получить прайс без ключей
            try:
                price = await api.post_values_keys(
                    subcategory__name=message.text,
                    key_dict={}
                )
                if price['text'].replace('\n', ''):
                    markup = await kb.get_product_kb()
                    return await send_to_user(
                        message=message,
                        text=price['text'],
                        images=[price['image']],
                        inline_keyboard=markup
                    )

            except:
                pass
            return await client.send_message(
                chat_id=message.from_user.id,
                text=text['Новые']['Меню']['Ключ']['404']
            )

        step = 1
        category__name = message.text
        await state.update_data(keys_list=keys_list)
        await state.update_data(category__name=category__name)
        await state.update_data(step=step)
        await state.update_data(step_choice={})
        await state.update_data(all_step=len(keys_list))
    else:
        keys_list: dict = data['keys_list']
        category__name: str = data['category__name']
        step: int = int(data['step'])

    key_name = [i for i in keys_list if i['order_id'] == step]
    key_name = key_name[0]['name'] if key_name else None
    if key_name:
        # Если шаг = 1, высылаем клавиатуру
        if step == 1:
            markup = await kb.kb_key_values(
                key_name=key_name,
                category__name=category__name,
            )
            if not markup:
                return await client.send_message(
                    chat_id=message.from_user.id,
                    text='Ничего не найдено'
                )
            await client.send_message(
                chat_id=message.from_user.id,
                text=text['Новые']['Меню']['Ключ']['Сообщение'] + ' ' + key_name,
                reply_markup=markup['keyboard']
            )
            v_category = data['v_category']
            v_category += markup['values']
            await state.update_data(v_category=v_category)
            await state.update_data(v_step=markup['values'])
            await state.update_data(step=2)
            await state.update_data(last_step_name=key_name)
            return

    ################################
    # Обновляем список выбранных ключей
    step_choice = data['step_choice']
    last_step_name = data['last_step_name']
    step_choice[last_step_name] = message.text
    await state.update_data(step_choice=step_choice)
    ################################
    # Гоняем циклом пока все ключи не указаны

    if int(len(keys_list)) + 1 != int(step):
        markup = await kb.kb_key_values_2(
            key_name=key_name,
            category__name=category__name,
            value=last_step_name
        )
        await client.send_message(
            chat_id=message.from_user.id,
            text=text['Новые']['Меню']['Ключ']['Сообщение'] + ' ' + key_name,
            reply_markup=markup['keyboard']
        )
        v_category = data['v_category']
        v_category += markup['values']
        await state.update_data(v_category=v_category)
        await state.update_data(v_step=markup['values'])
        await state.update_data(step=step + 1)

        await state.update_data(last_step_name=key_name)
        return
    data = await state.get_data()
    price = await api.post_values_keys(
        subcategory__name=category__name,
        key_dict=data['step_choice']
    )
    if not price:
        await client.send_message(
            chat_id=message.from_user.id,
            text=text['Новые']['Меню']['Прайс']['404'],
        )
        return

    markup = await kb.get_product_kb()
    await send_to_user(
        message=message,
        text=price['text'],
        images=[price['image']],
        inline_keyboard=markup
    )


################################
#Поиск
