# Generated by Django 4.1.4 on 2023-06-06 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parameter', '0028_alter_subcategorymodel_text'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productorderingmodel',
            options={'verbose_name': 'Порядок ключей', 'verbose_name_plural': 'Порядок ключей'},
        ),
        migrations.AlterModelOptions(
            name='subcategorymodel',
            options={'verbose_name': 'Подкатегории', 'verbose_name_plural': 'Подкатегории'},
        ),
        migrations.AddField(
            model_name='groupmodel',
            name='order_id',
            field=models.IntegerField(default=0, verbose_name='Порядковый номер'),
        ),
    ]
