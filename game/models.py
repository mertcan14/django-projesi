from django.db import models
from ckeditor.fields import RichTextField 

class Oyunlar(models.Model):
    oyun_isim=models.CharField(
        verbose_name="Oyun İsmi..",
        max_length=70,
    )
    bilgisayar_platform= models.BooleanField(
        default=False,
        verbose_name="Bilgisayar",
    )
    mobil_platform= models.BooleanField(
        default=False,
        verbose_name="Mobil"
    )
    konsol_platform= models.BooleanField(
        default=False,
        verbose_name="Oyun Konsolu",
    )
    kategoriler= models.CharField(
        max_length=200,
        verbose_name="Katogoriler",
    )
    geliştirici= models.CharField(
        max_length=200,
        verbose_name="Geliştirici",
    )
    cıkıs_tarih=models.DateField(
        verbose_name="Oyun Çıkış Tarihi"
    )
    türkce_dil=models.BooleanField(
        default=False,
        verbose_name="Türkçe Dil"
    )
    hakkında=RichTextField()
    game_image=models.ImageField(
        blank= True,
        null=True,
        verbose_name="Fotoğraf"
    )
# Create your models here.
