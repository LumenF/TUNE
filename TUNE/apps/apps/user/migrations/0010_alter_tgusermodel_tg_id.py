# Generated by Django 4.1.4 on 2023-05-23 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_alter_tgusermodel_last_login'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tgusermodel',
            name='tg_id',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='ID телеграм'),
        ),
    ]
