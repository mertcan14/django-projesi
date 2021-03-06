# Generated by Django 3.1 on 2020-10-21 11:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0005_auto_20201019_1253'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportForum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('toplam', models.CharField(max_length=100)),
                ('datereport', models.DateTimeField(auto_now=True, verbose_name='Report Tarih')),
                ('sorun', models.CharField(choices=[('yanlısbilgi', 'Yanlış Bilgi İçeriyor'), ('cinseliçerik', '18 Yaş Üstü Uygunsuz İçerik'), ('spam', 'Spam'), ('nefretvekötü', 'Nefret ve Kötü Amaçlı')], default='Seçmedi', max_length=100, verbose_name='Sebep')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.forum')),
                ('reportlayan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
