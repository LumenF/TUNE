# Generated by Django 4.1.4 on 2023-06-03 23:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parameter', '0022_subcategorymodel_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='keymodel',
            name='order_id',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(8)], verbose_name='Порядковый номер'),
        ),
        migrations.AlterField(
            model_name='subcategorymodel',
            name='order_id',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(8)], verbose_name='Порядковый номер'),
        ),
    ]
