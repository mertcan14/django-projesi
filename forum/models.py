from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField 
from game.models import Oyunlar
# Create your models here.
Report_CHOICES =(
    ('yanlısbilgi', 'Yanlış Bilgi İçeriyor'),
    ('cinseliçerik', '18 Yaş Üstü Uygunsuz İçerik'),
    ('spam', 'Spam'),
    ('nefretvekötü', 'Nefret ve Kötü Amaçlı'),
)

class Forum(models.Model):
    soran= models.ForeignKey("auth.User", on_delete=models.CASCADE)
    title=models.CharField(
        max_length=200,
        verbose_name="Başlık",
    )
    oyun=models.CharField(
        max_length=70,
        verbose_name="Oyun ismi",
        blank=True,
        null=True,
    )
    sorulanTarih=models.DateTimeField(
        verbose_name="Doğum Günü",
        auto_now=True,
    )
    soru=RichTextField()
    BegenmeSayısı=models.CharField(
        max_length=100,
        default=0,
    )
    YorumSayısı=models.CharField(
        max_length=100,
        default=0
    )

class Yorumforum(models.Model):
    yorumYapan=models.ForeignKey("auth.User", on_delete=models.CASCADE)
    yorumForm= models.ForeignKey(Forum, on_delete=models.CASCADE)
    dateyorum= models.DateTimeField(
        verbose_name="Yorum Tarih",
        auto_now=True,
    )
    yorum= models.CharField(
        max_length=400,
        verbose_name="Yorumu"
    )

class LikeYorum(models.Model):
    yorum=models.ForeignKey(Yorumforum, on_delete=models.CASCADE)
    datelike=models.DateTimeField(
        verbose_name="Beğenme Tarih",
        auto_now=True,
    )
    yorumbegenen=models.ForeignKey(User,on_delete=models.CASCADE)
    toplam=models.CharField(
        max_length=100
    )

class LikeForum(models.Model):
    like=models.ForeignKey(Forum, on_delete=models.CASCADE)
    begenen=models.ForeignKey(User, on_delete=models.CASCADE)
    toplam=models.CharField(
        max_length=100
    )
    datelike=models.DateTimeField(
        verbose_name="Beğenme Tarihi",
        auto_now=True
    )

class ReportForum(models.Model):
    report=models.ForeignKey(Forum, on_delete=models.CASCADE)
    reportlayan=models.ForeignKey(User, on_delete=models.CASCADE)
    toplam=models.CharField(
        max_length=100
    )
    datereport=models.DateTimeField(
        verbose_name="Report Tarih",
        auto_now=True,
    )
    sorun=models.CharField(
        max_length=100,
        choices=Report_CHOICES,
        default="Seçmedi",
        verbose_name="Sebep"
    )