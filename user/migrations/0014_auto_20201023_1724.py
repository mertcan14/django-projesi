# Generated by Django 3.1 on 2020-10-23 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_auto_20201023_1720'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mygame',
            name='dategame',
        ),
        migrations.AddField(
            model_name='mygame',
            name='date',
            field=models.DateTimeField(auto_now=True, verbose_name='Ekle Tarih'),
        ),
    ]
