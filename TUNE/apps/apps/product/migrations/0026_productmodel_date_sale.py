# Generated by Django 4.2.2 on 2023-07-03 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0025_favoritessubcategorymodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='productmodel',
            name='date_sale',
            field=models.DateField(blank=True, null=True, verbose_name='Дата продажи'),
        ),
    ]
