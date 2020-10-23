from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils import timezone
from django.db.models.signals import post_save
from game.models import Oyunlar
# Create your models here.

Cinsiyet_CHOICES = (
    ('belirtmekistemiyor', 'Belirtmek İstemiyorum'),
    ('erkek','ERKEK'),
    ('kadın', 'KADIN'),
    
)

class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dogum_gunu=models.DateField(
        verbose_name="Doğum Günü",
        null=True,
        blank=True,
    )
    cinsiyet=models.CharField(
        max_length=20,
        choices=Cinsiyet_CHOICES,
        default='belirtmekistemiyor'
    )
    hakkında=models.TextField(
        max_length=400,
        verbose_name="hakkımda",
        null=True,
        blank=True,
    )
    location = models.CharField(
        max_length=30,
        blank=True,
        default="Bilgi girilmemiş.",
        verbose_name="Konum"
    )
    user_image=models.ImageField(
        blank= True,
        null=True,
        verbose_name="Fotoğrafınız"
    )
    def __str__(self):
        return self.user

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profil.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profil.save()

class Mygame(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    game = models.OneToOneField(Oyunlar, on_delete=models.CASCADE)
    toplam= models.CharField(
        max_length=80,
    )

class AddMyFriends(models.Model):
    eklenen = models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name="eklenen", related_name="arkadasekle")
    ekleyen = models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name="ekleyen", related_name="eklearkadas")
    toplam=models.CharField(
        max_length=80,
    )
    def __str__(self):
        return self.toplam

class BlockMyFriends(models.Model):
    bloklayan= models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name="bloklayan", related_name="arkadasblok")
    bloklanan= models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name="bloklanan", related_name="blokarkadas")
    toplam= models.CharField(
        max_length=80
    )

