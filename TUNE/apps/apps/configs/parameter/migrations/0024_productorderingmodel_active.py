# Generated by Django 4.1.4 on 2023-06-04 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parameter', '0023_keymodel_order_id_alter_subcategorymodel_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='productorderingmodel',
            name='active',
            field=models.BooleanField(default=False, verbose_name='Для навигации'),
        ),
    ]