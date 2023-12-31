# Generated by Django 4.1.4 on 2023-06-09 08:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geography', '0002_rename_countrymodel_citymodel'),
        ('product', '0019_alter_productmodel_amount'),
        ('logs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now=True, verbose_name='Дата')),
                ('count', models.IntegerField(default=0, verbose_name='Кол-во')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geography.citymodel', verbose_name='Город')),
            ],
            options={
                'verbose_name': 'Пользователи',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='ProductLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now=True, verbose_name='Дата')),
                ('count', models.IntegerField(default=0, verbose_name='Кол-во')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.productmodel', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Б/У Товары',
                'verbose_name_plural': 'Б/У Товары',
            },
        ),
    ]
