# Generated by Django 4.1.4 on 2023-06-04 00:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product_conf', '0005_productkitmodel'),
        ('product', '0009_newproductmodel_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='newproductmodel',
            name='subcategory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product_conf.productsubcategorymodel', verbose_name='Категория'),
        ),
    ]
