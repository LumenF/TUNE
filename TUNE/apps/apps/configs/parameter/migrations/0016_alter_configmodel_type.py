# Generated by Django 4.2.1 on 2023-05-14 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parameter', '0015_configmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configmodel',
            name='type',
            field=models.CharField(choices=[(bool, 'default')], max_length=10, verbose_name='Тип'),
        ),
    ]
