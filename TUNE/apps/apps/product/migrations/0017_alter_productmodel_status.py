# Generated by Django 4.1.4 on 2023-06-05 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0016_alter_productmodel_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productmodel',
            name='status',
            field=models.CharField(choices=[('0', 'Модерация'), ('1', 'Опубликовано'), ('sale', 'Скидка'), ('2', 'Забронировано'), ('3', 'Продано в телеграм'), ('4', 'Продано в инстаграм'), ('5', 'Продано в магазине')], default='0', max_length=50, verbose_name='Статус'),
        ),
    ]