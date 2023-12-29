# Generated by Django 4.1.4 on 2023-05-23 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_alter_tgusermodel_tg_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tgusermodel',
            name='tg_id',
            field=models.CharField(db_index=True, default=1, max_length=255, unique=True, verbose_name='ID телеграм'),
            preserve_default=False,
        ),
    ]
