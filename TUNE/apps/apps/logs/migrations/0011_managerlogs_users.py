# Generated by Django 4.2.2 on 2023-07-21 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0010_bookingproductlogs_managerlogs'),
    ]

    operations = [
        migrations.AddField(
            model_name='managerlogs',
            name='users',
            field=models.JSONField(null=True, verbose_name='Пользователи'),
        ),
    ]
