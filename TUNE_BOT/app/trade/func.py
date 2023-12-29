from aiogram import types
from aiogram.filters import Text, Command
from aiogram.fsm.context import FSMContext

import app.index.kb as kb

from conf.conf_bot import dp, text, client


@dp.message(Text(text=text['Trade-in']['Заголовок']))
@dp.message(Text(text=text['Trade-in']['Назад']))
async def index_trade(
        message: types.Message,
        state: FSMContext = None,
):
    await client.send_message(
        chat_id=message.from_user.id,
        text='Для оценки устройства напишите пожалуйста ответы на вопросы: ♻️'
             '\n\n1. Модель устройства, объем памяти?'
             '\n\n2. Когда и Где покупали?'
             '\n\n3. В каком состоянии внешне (есть ли сколы, вмятины на корпусе? Если имеются, приложите фото)'
             '\n\n4. Имеется ли комплект (Коробка/Адаптер/Лайтнинг/Наушники/ Документы о покупке)'
             '\n\n5. Был ли в ремонтах? Все ли работает?'
             '\n\n6. Процент износа аккумулятора (можно посмотреть в настройках)'
    )
