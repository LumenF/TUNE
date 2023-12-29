# Generated by Django 4.2.2 on 2023-12-22 03:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geography', '0012_suppprovidermodel_site_id'),
        ('parameter', '0033_alter_subcategorymodel_amount_sale'),
        ('product', '0037_newproductmodel_tilda_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='newproductmodel',
            name='provider',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='geography.suppprovidermodel', verbose_name='Поставщик'),
        ),
        migrations.AlterField(
            model_name='newproductmodel',
            name='subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='parameter.subcategorymodel', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='newproductmodel',
            name='tilda_id',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ID Тильды'),
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='amount_buy',
            field=models.BigIntegerField(help_text='Цена закупки без наценки.', verbose_name='Цена закупки'),
        ),
    ]