# Generated by Django 4.2.2 on 2023-07-19 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geography', '0009_alter_invitemodel_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='pointscsvmodel',
            name='save_file',
            field=models.BooleanField(default=False),
        ),
    ]
