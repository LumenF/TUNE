# Generated by Django 4.2.1 on 2023-05-13 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parameter', '0011_remove_subcategorymodel_mask_extra_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategorymodel',
            name='amount',
            field=models.ImageField(default=1000, upload_to='', verbose_name='Наценка'),
        ),
    ]
