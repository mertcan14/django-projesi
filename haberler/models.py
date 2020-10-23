from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

Report_CHOICES =(
    ('yanlısbilgi', 'Yanlış Bilgi İçeriyor'),
    ('cinseliçerik', '18 Yaş Üstü Uygunsuz İçerik'),
    ('spam', 'Spam'),
    ('nefretvekötü', 'Nefret ve Kötü Amaçlı'),
)

class Haber(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    baslik=models.CharField(
        verbose_name="Başlık",
        max_length=250,
    )
    content=RichTextField()
    tarih=models.DateTimeField(
        verbose_name="Eklenme Tarihi",
        auto_now=True,
    )
    tags=models.CharField(
        verbose_name="Kategoriler",
        max_length=175,
    )
    haber_image=models.ImageField(
        verbose_name="Fotoğraf",
    )
    toplamBegenme=models.CharField(
        max_length=100,
        default=0
    )
    toplamYorum=models.CharField(
        max_length=100,
        default=0
    )
class YorumHaber(models.Model):
    yorumYapan=models.ForeignKey("auth.User",on_delete=models.CASCADE)
    yorumHaber=models.ForeignKey(Haber, on_delete=models.CASCADE)
    dateyorum=models.DateTimeField(
        verbose_name="Yorum Tarih",
        auto_now=True,
    )
    yorum=models.CharField(
        max_length=400,
        verbose_name="Yorum",
    )
class LikeYorumHaber(models.Model):
    yorum=models.ForeignKey(YorumHaber, on_delete=models.CASCADE)
    datelike=models.DateTimeField(
        verbose_name="Beğenme Tarih",
        auto_now=True
    )
    yorumbegenen=models.ForeignKey(User, on_delete=models.CASCADE)
    toplam=models.CharField(
        max_length=100
    )
class AddFavoriHaber(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    haber=models.ForeignKey(Haber, on_delete=models.CASCADE)
    datefav=models.DateTimeField(
        verbose_name="Beğenme Tarih",
        auto_now=True
    )
    toplam=models.CharField(
        max_length=100
    )

class AddReportHaber(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    haber=models.ForeignKey(Haber, on_delete=models.CASCADE)
    daterep=models.DateTimeField(
        verbose_name="Raport Tarih",
        auto_now=True
    )
    toplam=models.CharField(
        max_length=100
    )
    sorun=models.CharField(
        max_length=100,
        choices=Report_CHOICES,
        default="Seçmedi",
        verbose_name="Sebep"
    )
# Create your models here.
