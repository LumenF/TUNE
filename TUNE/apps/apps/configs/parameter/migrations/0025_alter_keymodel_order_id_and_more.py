# Generated by Django 4.1.4 on 2023-06-04 02:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parameter', '0024_productorderingmodel_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keymodel',
            name='order_id',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(8)], verbose_name='Порядковый номер'),
        ),
        migrations.AlterField(
            model_name='productorderingmodel',
            name='order_id',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(4)], verbose_name='Порядковый номер'),
        ),
        migrations.AlterField(
            model_name='subcategorymodel',
            name='order_id',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(8)], verbose_name='Порядковый номер'),
        ),
    ]
