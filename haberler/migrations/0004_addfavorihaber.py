# Generated by Django 3.1 on 2020-10-16 11:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('haberler', '0003_likeyorumhaber'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddFavoriHaber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datefav', models.DateTimeField(auto_now=True, verbose_name='Beğenme Tarih')),
                ('toplam', models.CharField(max_length=100)),
                ('haber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='haberler.haber')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
