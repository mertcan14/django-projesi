# Generated by Django 3.1 on 2020-10-16 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('haberler', '0006_auto_20201016_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='haber',
            name='toplamBegenme',
            field=models.CharField(default=0, max_length=100),
        ),
    ]
