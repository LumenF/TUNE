# Generated by Django 4.2.2 on 2023-06-23 04:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('site_product', '0007_shoptypemodel_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopKeyModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now=True, verbose_name='Дата создания')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('key', models.CharField(max_length=255, verbose_name='Тип')),
                ('value', models.CharField(max_length=255, verbose_name='Значение')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='site_product.shopproductmodel', verbose_name='Тип')),
            ],
            options={
                'verbose_name': 'Ключ',
                'verbose_name_plural': 'Ключи',
            },
        ),
    ]