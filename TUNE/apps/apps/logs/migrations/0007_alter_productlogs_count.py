# Generated by Django 4.2.2 on 2023-07-03 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0006_alter_productlogs_date_created_amountproductlogs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productlogs',
            name='count',
            field=models.IntegerField(default=1, verbose_name='Кол-во'),
        ),
    ]