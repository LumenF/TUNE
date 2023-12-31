# Generated by Django 4.2.1 on 2023-05-06 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parameter', '0007_subcategorymodel_keys'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subcategorymodel',
            name='keys',
        ),
        migrations.AddField(
            model_name='categorymodel',
            name='keys',
            field=models.ManyToManyField(to='parameter.typekeymodel', verbose_name='Ключи'),
        ),
        migrations.AlterField(
            model_name='subcategorymodel',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parameter.categorymodel', verbose_name='Категория'),
        ),
    ]
