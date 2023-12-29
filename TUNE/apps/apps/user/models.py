from typing import Union

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import QuerySet

from apps.abstraction.models import AbstractModel, nb


class UserModel(AbstractUser):
    class Meta:
        verbose_name = 'Администрация'
        verbose_name_plural = 'Администрация'

    city = models.ForeignKey(
        verbose_name='Город',
        to='geography.CityModel',
        on_delete=models.CASCADE,
    )
    tg_id = models.CharField(
        verbose_name='ID Телеграм',
        max_length=255,
        default=0
    )
    report = models.BooleanField(
        verbose_name='Отчеты',
        default=False,
        help_text='Получение отчетов в конце дня.'
    )
    notice = models.BooleanField(
        verbose_name='Уведомления',
        default=False,
        help_text='Получение уведомлений о создании товаров поставщиками'
    )


class TgUserModel(AbstractModel):
    class Meta:
        verbose_name = 'Телеграм'
        verbose_name_plural = 'Телеграм'

    tg_id = models.CharField(
        verbose_name='ID телеграм',
        unique=True,
        db_index=True,
        max_length=255,
    )

    username = models.CharField(
        verbose_name='Ник',
        max_length=255,
        **nb
    )

    first_name = models.CharField(
        verbose_name='Имя',
        max_length=255,
        **nb
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=255,
        **nb
    )

    phone = models.CharField(
        verbose_name='Телефон',
        max_length=255,
        **nb
    )
    email = models.CharField(
        verbose_name='Почта',
        max_length=255,
        **nb
    )
    is_blocked_bot = models.BooleanField(
        verbose_name='Заблокировал бота',
        default=False,
    )

    is_staff = models.BooleanField(
        verbose_name='Статус админа',
        default=False,
    )
    is_ban_user = models.BooleanField(
        verbose_name='Заблокирован',
        default=False
    )
    last_login = models.DateTimeField(
        verbose_name='Последняя сессия',
        auto_now=True,
        null=True
    )
    city = models.ForeignKey(
        verbose_name='Город',
        to='geography.CityModel',
        on_delete=models.CASCADE,
        default=1
    )

    notice = models.BooleanField(
        verbose_name='Уведомления',
        default=True,
    )

    segment = models.ManyToManyField(
        verbose_name='Сегменты',
        to='mailing.SegmentationModel',
        blank=True,
    )

    def __str__(self):
        if self.username:
            return '@' + self.username
        if self.first_name or self.last_name:
            name = ' ' + self.first_name if self.first_name else ''
            name += ' ' + self.last_name if self.last_name else ''
            return name
        return self.tg_id
