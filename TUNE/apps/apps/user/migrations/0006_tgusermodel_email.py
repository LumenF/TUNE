# Generated by Django 4.2.1 on 2023-05-23 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_remove_usermodel_bio_usermodel_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='tgusermodel',
            name='email',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Почта'),
        ),
    ]
