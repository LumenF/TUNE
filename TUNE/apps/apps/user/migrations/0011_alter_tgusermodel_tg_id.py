# Generated by Django 4.1.4 on 2023-05-23 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_alter_tgusermodel_tg_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tgusermodel',
            name='tg_id',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, unique=True, verbose_name='ID телеграм'),
        ),
    ]
