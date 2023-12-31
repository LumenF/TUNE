# Generated by Django 4.2.2 on 2023-07-03 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geography', '0003_alter_citymodel_date_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='InviteModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now=True, verbose_name='Дата создания')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('name', models.CharField(max_length=100, verbose_name='Ссылка')),
                ('count', models.BigIntegerField(default=0, verbose_name='Счетчик')),
            ],
            options={
                'verbose_name': 'Рефералы',
                'verbose_name_plural': 'Рефералы',
            },
        ),
    ]
