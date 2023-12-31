# Generated by Django 4.2.2 on 2023-09-09 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0033_newpricesearchmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='newproductmodel',
            name='amount_sale',
            field=models.CharField(default=0, max_length=255, verbose_name='Скидка'),
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='name',
            field=models.CharField(db_index=True, help_text='Название должно содержать конечную цену<br><br>Цена не должна содержать пробелы<br><br>Для перечеркивания цены, оберните её в ^1000^<br><br>🔥 ⚡️ 💥 ₽ 🔻 ✅ 🔝', max_length=90, verbose_name='Название'),
        ),
    ]
