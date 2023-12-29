# Generated by Django 4.2.2 on 2023-07-03 13:35

import apps.apps.mailing.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0004_alter_mailingallmodel_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailingCityModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Тема сообщения')),
                ('image_1', models.ImageField(blank=True, null=True, upload_to=apps.apps.mailing.models.path_mailing, verbose_name='Изображение 1')),
                ('text', models.TextField(blank=True, help_text='Поддерживается базовая HTML разметка<br><br>Максимум 1024 символа', max_length=1024, null=True, verbose_name='Текст')),
                ('count_success', models.IntegerField(default=0, verbose_name='Доставлено')),
                ('count_fail', models.IntegerField(default=0, verbose_name='Ошибки')),
                ('count_all', models.IntegerField(default=0, verbose_name='Всего')),
                ('status', models.CharField(choices=[('0', 'Не отправлено'), ('1', 'Процесс'), ('2', 'Завершено'), ('3', 'Прервано'), ('4', 'Внутренняя ошибка')], default='0', max_length=255, verbose_name='Статус')),
                ('date_send', models.DateTimeField(blank=True, null=True, verbose_name='Дата отправки')),
                ('redis_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='Идентификатор')),
            ],
            options={
                'verbose_name': 'Рассылка городу',
                'verbose_name_plural': 'Рассылка городу',
            },
        ),
        migrations.RemoveField(
            model_name='mailingallmodel',
            name='image_2',
        ),
        migrations.RemoveField(
            model_name='mailingallmodel',
            name='image_3',
        ),
    ]