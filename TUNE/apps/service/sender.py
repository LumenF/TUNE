import requests
from telebot import TeleBot, types

from TUNE.settings import AWS_PATH

MEDIA_PATH = 'https://2481cb39-1f5a3cd1-6620-459a-860f-6d8d44288631.s3.timeweb.com/tune/media/'


def send_text(
        client: TeleBot,
        user_id: str,
        text: str,
        keyboard=None,

) -> True or False:
    try:
        client.send_message(
            chat_id=user_id,
            text=text,
            reply_markup=keyboard
        )
        return True
    except:
        return False


def send_text_and_photo(
        client: TeleBot,
        user_id: str,
        text: str,
        photo,
        keyboard=None
) -> True or False:
    try:
        client.send_photo(
            chat_id=user_id,
            photo=photo,
            caption=text,
            reply_markup=keyboard
        )
        return True
    except:
        return False

def sender_master(
        client: TeleBot,
        user_list: list or set,
        text: str,
        photo: str = None,
        keyboard=None,
        model=None,
        text_2=None
):
    count = 0
    mail_success = 0
    user_success = []

    mail_fail = 0
    users_fail = []
    if text and not photo:
        for user in user_list:
            count += 1
            result = send_text(
                client=client,
                user_id=user,
                text=text,
                keyboard=keyboard
            )
            if text_2:
                send_text(
                    client=client,
                    user_id=user,
                    text=text_2,
                )
            if result:
                mail_success += 1
                user_success.append(user)
            else:
                mail_fail += 1
                users_fail.append(user)
            if count % 1 == 0:
                if model:
                    model.update(count_success=mail_success)
                    model.update(count_fail=mail_fail)

        return {
            'mail_success': mail_success,
            'user_success': user_success,
            'mail_fail': mail_fail,
            'users_fail': users_fail
        }
    if text and photo:
        for user in user_list:
            count += 1

            result = send_text_and_photo(
                client=client,
                user_id=user,
                photo=photo,
                text=text,
                keyboard=keyboard
            )
            if text_2:
                send_text(
                    client=client,
                    user_id=user,
                    text=text_2,
                )
            if result:
                mail_success += 1
                user_success.append(user)
            else:
                mail_fail += 1
                users_fail.append(user)
            if count % 1 == 0:
                if model:
                    model.update(count_success=mail_success)
                    model.update(count_fail=mail_fail)
        return {
            'mail_success': mail_success,
            'user_success': user_success,
            'mail_fail': mail_fail,
            'users_fail': users_fail
        }
