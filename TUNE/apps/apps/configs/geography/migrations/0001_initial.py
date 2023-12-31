# Generated by Django 4.2.1 on 2023-05-03 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CountryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True, verbose_name='Дата создания')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
            },
        ),
    ]
