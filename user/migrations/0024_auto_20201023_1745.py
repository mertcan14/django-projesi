# Generated by Django 3.1 on 2020-10-23 14:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game', '0001_initial'),
        ('user', '0023_delete_addgamemy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mygame',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.oyunlar'),
        ),
        migrations.AlterField(
            model_name='mygame',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
