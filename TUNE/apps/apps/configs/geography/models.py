import csv
import datetime
import time
import urllib.request
from pprint import pprint

import requests
from django.db import models

from TUNE.settings import TUNE_BASE_URL
from apps.abstraction.models import AbstractModel, nb
from apps.apps.product.models import NewProductModel


def path_invited(
        instance,
        filename
):
    return 'invited/{0}'.format(
        filename
    )


def file_bonus(
        instance,
        filename
):
    return 'file_bonus/files/{0}'.format(
        filename
    )


class CityModel(AbstractModel):
    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    name = models.CharField(
        verbose_name='Название',
        max_length=100,
    )

    def __str__(self):
        return self.name


class InviteModel(AbstractModel):
    class Meta:
        verbose_name = 'Рефералы'
        verbose_name_plural = 'Рефералы'

    name = models.CharField(
        verbose_name='Имя реферала',
        max_length=100,
        help_text='Имя указывать на английском!'
                  '<br>'
                  '<br>'
                  'Ссылка: https://t.me/TuneBot_bot?start=ИМЯ_РЕФЕРАЛА'
    )
    count = models.BigIntegerField(
        verbose_name='Счетчик',
        default=0
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to=path_invited,
    )

    def __str__(self):
        return self.name

    def increase_count(self):
        self.count += 1
        self.save_base()


class PointsModel(models.Model):
    class Meta:
        verbose_name = 'Значения баллов'
        verbose_name_plural = 'Значения баллов'

    name = models.CharField(
        verbose_name='ФИО',
        max_length=100,
        **nb
    )
    phone = models.CharField(
        verbose_name='Телефон',
        max_length=20,
    )

    value = models.CharField(
        verbose_name='Бонусы',
        max_length=100
    )

    buy = models.CharField(
        verbose_name='Сумма покупок',
        max_length=100
    )

    buy_frozen = models.CharField(
        verbose_name='Отложено',
        max_length=100
    )

    def __str__(self):
        return self.phone


class PointsCSVModel(models.Model):
    class Meta:
        verbose_name = 'Баллы'
        verbose_name_plural = 'Баллы'

    file = models.FileField(
        verbose_name='Файл',
        upload_to=file_bonus
    )

    date_created = models.DateField(
        verbose_name='Дата создания',
        auto_now=True
    )
    save_file = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.date_created)

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.save_base(
            using=using,
            force_insert=force_insert,
            force_update=force_update,
            update_fields=update_fields,
        )
        url = self.file.url
        response = urllib.request.urlopen(url)
        lines = [i.decode('utf-8') for i in response.readlines()]
        reader = csv.DictReader(lines, delimiter=';')
        data = []
        for row in reader:
            row: dict
            data.append({
                'Имя': row['Имя'] if 'Имя' in row else '---',
                'Логин': row['Логин'],
                'Бонусы': row['Количество бонусов'] if 'Количество бонусов' in row else '0',
                'Сумма': row['Сумма покупок'] if 'Сумма покупок' in row else '0',
                'Отложено': row['Количество отложенных бонусов'] if 'Количество отложенных бонусов' in row else '0',
            })
        new = []

        for i in data:
            new.append(
                PointsModel(
                    name=i['Имя'],
                    phone=i['Логин'],
                    value=i['Бонусы'],
                    buy=i['Сумма'],
                    buy_frozen=i['Отложено'],
                )
            )
        PointsModel.objects.all().delete()
        PointsModel.objects.bulk_create(new)


class SuppProviderModel(models.Model):
    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

    name = models.CharField(
        verbose_name='Имя',
        max_length=255,
    )

    SITE_ID = models.IntegerField(
        verbose_name='ID на сайте',
        null=True,
        blank=True
    )
    def __str__(self):
        return self.name

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.SITE_ID:
            self.save_base(
                using=using,
                force_insert=force_insert,
                force_update=force_update,
                update_fields=update_fields,
            )
        if not self.SITE_ID:
            url = f'{TUNE_BASE_URL}index.php?route=api/all/update_supplier&token=A0kwh2L8KRzha3zicpT6VJYEMq47RTU7'
            result = requests.post(
                url=url,
                json={
                    'supplier_id': 0,
                    'name': self.name
                },
            )
            if result.status_code == 200:
                self.SITE_ID = result.json()['supplier_id']
                self.save_base(
                    using=using,
                    force_insert=force_insert,
                    force_update=force_update,
                    update_fields=update_fields,
                )
        else:
            url = f'{TUNE_BASE_URL}index.php?route=api/all/update_supplier&token=A0kwh2L8KRzha3zicpT6VJYEMq47RTU7'
            requests.post(
                url=url,
                json={
                    'supplier_id': self.id,
                    'name': self.name,
                },
            )

        q = NewProductModel.objects.filter(provider=self)
        for i in q:
            if i.params and i.params['Поставщик'] != self.name:
                i.params['Поставщик'] = self.name
                i.save()