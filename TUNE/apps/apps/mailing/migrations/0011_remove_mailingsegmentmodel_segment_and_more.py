# Generated by Django 4.2.2 on 2023-07-09 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0010_mailingsegmentmodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailingsegmentmodel',
            name='segment',
        ),
        migrations.AddField(
            model_name='mailingsegmentmodel',
            name='segment',
            field=models.ManyToManyField(to='mailing.segmentationmodel', verbose_name='Город'),
        ),
    ]
