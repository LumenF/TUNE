# Generated by Django 4.2.1 on 2023-05-06 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parameter', '0006_keymodel_subcategory_alter_categorymodel_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategorymodel',
            name='keys',
            field=models.ManyToManyField(to='parameter.typekeymodel', verbose_name='Ключи'),
        ),
    ]
