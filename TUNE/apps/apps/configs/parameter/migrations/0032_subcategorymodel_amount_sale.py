# Generated by Django 4.2.2 on 2023-09-10 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parameter', '0031_alter_categorymodel_date_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategorymodel',
            name='amount_sale',
            field=models.IntegerField(default=0, verbose_name='Скидка'),
        ),
    ]