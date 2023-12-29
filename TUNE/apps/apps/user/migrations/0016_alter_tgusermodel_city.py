# Generated by Django 4.1.4 on 2023-06-09 08:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geography', '0002_rename_countrymodel_citymodel'),
        ('user', '0015_tgusermodel_notice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tgusermodel',
            name='city',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='geography.citymodel', verbose_name='Город'),
        ),
    ]