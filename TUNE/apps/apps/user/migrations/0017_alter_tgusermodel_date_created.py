# Generated by Django 4.1.4 on 2023-06-10 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0016_alter_tgusermodel_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tgusermodel',
            name='date_created',
            field=models.DateField(auto_now=True, verbose_name='Дата создания'),
        ),
    ]
