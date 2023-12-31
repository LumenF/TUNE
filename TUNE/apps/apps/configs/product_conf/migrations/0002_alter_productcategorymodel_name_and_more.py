# Generated by Django 4.1.4 on 2023-05-23 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_conf', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcategorymodel',
            name='name',
            field=models.CharField(db_index=True, max_length=255, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='productguaranteemodel',
            name='name',
            field=models.CharField(db_index=True, max_length=255, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='productsubcategorymodel',
            name='name',
            field=models.CharField(db_index=True, max_length=255, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='producttypemodel',
            name='name',
            field=models.CharField(db_index=True, max_length=255, verbose_name='Название'),
        ),
    ]
