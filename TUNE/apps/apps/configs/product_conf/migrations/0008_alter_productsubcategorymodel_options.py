# Generated by Django 4.2.2 on 2023-07-14 10:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product_conf', '0007_alter_productkitmodel_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productsubcategorymodel',
            options={'ordering': ('name', 'order_id'), 'verbose_name': 'Подкатегория', 'verbose_name_plural': 'Подкатегории'},
        ),
    ]