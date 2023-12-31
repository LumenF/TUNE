# Generated by Django 4.2.2 on 2023-07-22 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geography', '0011_suppprovidermodel'),
        ('product', '0031_productmodel_code_alter_productmodel_create'),
    ]

    operations = [
        migrations.AddField(
            model_name='pricemodel',
            name='provider',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='geography.suppprovidermodel', verbose_name='Поставщик'),
            preserve_default=False,
        ),
    ]
