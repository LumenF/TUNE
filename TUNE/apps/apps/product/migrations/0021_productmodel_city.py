# Generated by Django 4.2.2 on 2023-06-11 05:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geography', '0003_alter_citymodel_date_created'),
        ('product', '0020_alter_favoritesmodel_date_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productmodel',
            name='city',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='geography.citymodel', verbose_name='Город'),
        ),
    ]
