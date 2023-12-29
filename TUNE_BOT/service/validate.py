import functools

from aiogram import types
from aiogram.fsm.context import FSMContext


from conf.conf_bot import client


def validate_keyboard(value: str, back: str, back_2: str = 'x2qs',  back_3: str = 'x{2',):
    def decorator(function):
        @functools.wraps(function)
        async def wrapper(message: types.Message,
                          state: FSMContext = None,
                          *args, **kwargs
                          ):
            from app.bitrix.func import bitrix_valid
            args = [message, state][:function.__code__.co_argcount]
            data = await state.get_data()

            try:
                if not message.text:
                    return await bitrix_valid(message=message)
                elif data and message.text not in data[value] \
                        and message.text != back \
                        and message.text != back_2 \
                        and back_3 not in message.text:
                    # await client.send_message(
                    #     chat_id=message.from_user.id,
                    #     text='Сообщение отправлено в битрикс',
                    # )

                    await bitrix_valid(message=message)
                    raise ValueError
            except ValueError as er:
                return

            msg = await function(*args)

            return msg

        return wrapper

    return decorator
