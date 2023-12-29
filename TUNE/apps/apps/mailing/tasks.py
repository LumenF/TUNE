from telebot import types

from TUNE.celery_conf import app
from TUNE.settings import client
from apps.apps.mailing.dd import last_users

from apps.apps.mailing.models import MailingAllModel, MailingCityModel, SegmentationReadyModel, MailingSegmentModel
from apps.apps.user.models import TgUserModel
from apps.service.sender import sender_master


@app.task()
def mail_all(
        _id: str or int,
):
    mail = MailingAllModel.objects.get(id=_id)
    model = MailingAllModel.objects.filter(id=_id)

    user_list = list(str(i['tg_id']) for i in TgUserModel.objects.all().values('tg_id'))
    user_list = set(last_users + user_list)
    keyboard = []
    if mail.products.all():
        keyboard.append(
            [types.InlineKeyboardButton(text='Показать товары', callback_data='m_all.' + str(_id))]
        )
        keyboard = types.InlineKeyboardMarkup(keyboard=keyboard)
    MailingAllModel.objects.filter(id=_id).update(
        status='1',
    )

    model.update(count_all=len(user_list))
    sender_master(
        client=client,
        photo=mail.image_1.url if mail.image_1 else None,
        user_list=user_list,
        text=mail.text,
        model=model,
        keyboard=keyboard
    )
    MailingAllModel.objects.filter(id=_id).update(
        status='2',
    )


@app.task()
def mail_all_test(
        _id: str or int,
):
    mail = MailingAllModel.objects.get(id=_id)
    model = MailingAllModel.objects.filter(id=_id)

    user_list = set(i['tg_id'] for i in TgUserModel.objects.filter(is_staff=True).values('tg_id'))
    keyboard = []
    if mail.products.all():
        keyboard.append(
            [types.InlineKeyboardButton(text='Показать товары', callback_data='m_all.' + str(_id))]
        )
        keyboard = types.InlineKeyboardMarkup(keyboard=keyboard)
    sender_master(
        client=client,
        photo=mail.image_1.url if mail.image_1 else None,
        user_list=user_list,
        text=mail.text,
        model=model,
        keyboard=keyboard
    )


################################################################
# ГОРОДА


@app.task()
def mail_city(
        _id: str or int,
):
    mail = MailingCityModel.objects.get(id=_id)
    model = MailingCityModel.objects.filter(id=_id)

    user_list = set(i['tg_id'] for i in TgUserModel.objects.filter(city=mail.city).values('tg_id'))
    keyboard = []
    if mail.products.all():
        keyboard.append(
            [types.InlineKeyboardButton(text='Показать товары', callback_data='m_city.' + str(_id))]
        )
        keyboard = types.InlineKeyboardMarkup(keyboard=keyboard)
    MailingCityModel.objects.filter(id=_id).update(
        status='1',
    )

    model.update(count_all=len(user_list))
    sender_master(
        client=client,
        photo=mail.image_1.url if mail.image_1 else None,
        user_list=user_list,
        text=mail.text,
        model=model,
        keyboard=keyboard
    )
    MailingCityModel.objects.filter(id=_id).update(
        status='2',
    )


@app.task()
def mail_city_test(
        _id: str or int,
):
    mail = MailingCityModel.objects.get(id=_id)
    model = MailingCityModel.objects.filter(id=_id)

    user_list = set(i['tg_id'] for i in TgUserModel.objects.filter(is_staff=True).values('tg_id'))
    keyboard = []
    if mail.products.all():
        keyboard.append(
            [types.InlineKeyboardButton(text='Показать товары', callback_data='m_city.' + str(_id))]
        )
        keyboard = types.InlineKeyboardMarkup(keyboard=keyboard)
    sender_master(
        client=client,
        photo=mail.image_1.url if mail.image_1 else None,
        user_list=user_list,
        text=mail.text + '\n\nРассылка пройдет для города:\n' + mail.city.name,
        model=model,
        keyboard=keyboard,
    )


################################################################
# Сегменты

@app.task()
def mail_segment(
        _id: str or int,
):
    mail = MailingSegmentModel.objects.get(id=_id)
    model = MailingSegmentModel.objects.filter(id=_id)

    user_list = set(i['tg_id'] for i in TgUserModel.objects.filter(
        segment__in=mail.segment.all()
    ).values('tg_id'))
    keyboard = []
    if mail.products.all():
        keyboard.append(
            [types.InlineKeyboardButton(text='Показать товары', callback_data='m_city.' + str(_id))]
        )
        keyboard = types.InlineKeyboardMarkup(keyboard=keyboard)
    MailingSegmentModel.objects.filter(id=_id).update(
        status='1',
    )

    model.update(count_all=len(user_list))
    sender_master(
        client=client,
        photo=mail.image_1.url if mail.image_1 else None,
        user_list=user_list,
        text=mail.text,
        model=model,
        keyboard=keyboard
    )
    MailingSegmentModel.objects.filter(id=_id).update(
        status='2',
    )

@app.task()
def mail_segment_test(
        _id: str or int,
):
    mail = MailingSegmentModel.objects.get(id=_id)
    model = MailingSegmentModel.objects.filter(id=_id)

    user_list = set(i['tg_id'] for i in TgUserModel.objects.filter(is_staff=True).values('tg_id'))
    keyboard = []
    if mail.products.all():
        keyboard.append(
            [types.InlineKeyboardButton(text='Показать товары', callback_data='m_city.' + str(_id))]
        )
        keyboard = types.InlineKeyboardMarkup(keyboard=keyboard)
    sender_master(
        client=client,
        photo=mail.image_1.url if mail.image_1 else None,
        user_list=user_list,
        text=mail.text,
        model=model,
        keyboard=keyboard,
    )


################################################################
# Опрос сегмента


@app.task()
def mail_q_segment(
        _id: str or int,
        text: str
):
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(types.InlineKeyboardButton("Пройти опрос!", callback_data="segment." + str(_id)))
    users = set(i['tg_id'] for i in TgUserModel.objects.all().values('tg_id'))
    user_ready = set(
        i['user__tg_id'] for i in SegmentationReadyModel.objects.filter(base__id=_id).values('user__tg_id'))
    user_list = [i for i in users if i not in user_ready]
    sender_master(
        client=client,
        user_list=user_list,
        text=text,
        keyboard=markup
        )

@app.task()
def mail_q_segment_test(
        _id: str or int,
        text: str
):
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(types.InlineKeyboardButton("Пройти опрос!", callback_data="segment." + str(_id)))
    users = set(i['tg_id'] for i in TgUserModel.objects.filter(is_staff=True).values('tg_id'))

    sender_master(
        client=client,
        user_list=users,
        text=text,
        keyboard=markup
        )