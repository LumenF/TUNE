# Generated by Django 4.1.4 on 2023-05-23 18:48

import apps.apps.product.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('parameter', '0017_alter_configmodel_type'),
        ('product_conf', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('geography', '0002_rename_countrymodel_citymodel'),
        ('user', '0009_alter_tgusermodel_last_login'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True, verbose_name='Дата создания')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('image_1', models.ImageField(upload_to=apps.apps.product.models.save_path, verbose_name='Картинка')),
                ('image_2', models.ImageField(blank=True, null=True, upload_to=apps.apps.product.models.save_path, verbose_name='Картинка')),
                ('image_3', models.ImageField(blank=True, null=True, upload_to=apps.apps.product.models.save_path, verbose_name='Картинка')),
                ('name', models.CharField(db_index=True, help_text='Название должно содержать цену<br><br>Цена не должна содержать пробелы', max_length=50, verbose_name='Название')),
                ('amount', models.CharField(blank=True, max_length=15, null=True, verbose_name='Цена')),
                ('amount_sale', models.IntegerField(default=0, verbose_name='Скидка')),
                ('status', models.CharField(choices=[('0', 'Модерация'), ('1', 'Опубликовано'), ('2', 'Забронировано'), ('3', 'Продано в телеграм'), ('4', 'Продано в инстаграм'), ('5', 'Продано в магазине')], default='0', max_length=50, verbose_name='Статус')),
                ('text', models.TextField(blank=True, help_text='Оставить поле пустым, если не требуется.', max_length=700, null=True, verbose_name='Произведенные работы:')),
                ('caption', models.TextField(blank=True, max_length=1024, null=True, verbose_name='Итоговый текст')),
                ('author', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('guarantee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_conf.productguaranteemodel', verbose_name='Гарантия')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_conf.productstatemodel', verbose_name='Состояние')),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_conf.productsubcategorymodel', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='PriceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True, verbose_name='Дата создания')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('text', models.TextField(verbose_name='Прайс')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parameter.categorymodel', verbose_name='Категории товаров')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geography.citymodel', verbose_name='Регион прайса')),
            ],
            options={
                'verbose_name': 'Прайс',
                'verbose_name_plural': 'Прайсы',
            },
        ),
        migrations.CreateModel(
            name='FavoritesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True, verbose_name='Дата создания')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.productmodel', verbose_name='Товар')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.tgusermodel', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Избранное Б/У',
                'verbose_name_plural': 'Избранные Б/У',
            },
        ),
    ]
