# Generated by Django 4.1.4 on 2023-05-30 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_productmodel_kit'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewProductModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True, verbose_name='Дата создания')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('tilda_UID', models.CharField(max_length=255, verbose_name='Tilda UID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('price', models.CharField(max_length=255, verbose_name='Цена')),
            ],
            options={
                'verbose_name': 'Новые товары',
                'verbose_name_plural': 'Новые товары',
            },
        ),
    ]
