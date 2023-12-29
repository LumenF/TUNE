# Generated by Django 4.2.2 on 2023-06-15 20:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0017_alter_tgusermodel_date_created'),
        ('product_conf', '0006_alter_productcategorymodel_date_created_and_more'),
        ('product', '0024_alter_productmodel_guarantee'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavoritesSubcategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now=True, verbose_name='Дата создания')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_conf.productsubcategorymodel', verbose_name='Товар')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.tgusermodel', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Избранное категории Б/У',
                'verbose_name_plural': 'Избранные категории Б/У',
            },
        ),
    ]
