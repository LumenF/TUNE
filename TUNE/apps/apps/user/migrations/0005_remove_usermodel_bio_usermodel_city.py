# Generated by Django 4.2.1 on 2023-05-03 20:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geography', '0002_rename_countrymodel_citymodel'),
        ('user', '0004_remove_tgusermodel_is_bot'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermodel',
            name='bio',
        ),
        migrations.AddField(
            model_name='usermodel',
            name='city',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='geography.citymodel', verbose_name='Город'),
            preserve_default=False,
        ),
    ]
