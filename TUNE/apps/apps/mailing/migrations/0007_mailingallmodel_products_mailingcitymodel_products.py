# Generated by Django 4.2.2 on 2023-07-03 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0026_productmodel_date_sale'),
        ('mailing', '0006_mailingcitymodel_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailingallmodel',
            name='products',
            field=models.ManyToManyField(help_text='Оставьте пустым, если не требуется.', to='product.productmodel', verbose_name='Товары'),
        ),
        migrations.AddField(
            model_name='mailingcitymodel',
            name='products',
            field=models.ManyToManyField(help_text='Оставьте пустым, если не требуется.', to='product.productmodel', verbose_name='Товары'),
        ),
    ]