# Generated by Django 4.1.4 on 2023-06-03 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parameter', '0017_alter_configmodel_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategorymodel',
            name='mask_bot',
            field=models.ManyToManyField(blank=True, help_text='Пример:<br>', related_name='bot', to='parameter.typekeymodel', verbose_name='Ключи для бота'),
        ),
    ]
