# Generated by Django 4.1.4 on 2023-06-04 01:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_newproductmodel_subcategory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newproductmodel',
            name='params',
        ),
    ]
