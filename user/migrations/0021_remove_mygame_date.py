# Generated by Django 3.1 on 2020-10-23 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0020_auto_20201023_1735'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mygame',
            name='date',
        ),
    ]
