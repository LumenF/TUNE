# Generated by Django 4.2.2 on 2023-06-23 04:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('site_product', '0008_shopkeymodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopproductmodel',
            name='p_color',
        ),
        migrations.RemoveField(
            model_name='shopproductmodel',
            name='p_memory',
        ),
        migrations.RemoveField(
            model_name='shopproductmodel',
            name='p_size',
        ),
    ]