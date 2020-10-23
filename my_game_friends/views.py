from django.shortcuts import render
from game.models import Oyunlar
from haberler.models import Haber,AddFavoriHaber, YorumHaber
from forum.models import Forum, Yorumforum, LikeYorum, LikeForum
from user.models import AddMyFriends, User


def anasayfa(request):
    oyun_active=Oyunlar.objects.order_by("?").first()
    oyun=Oyunlar.objects.exclude(id=oyun_active.id).order_by("?")[:2]  
    haberlerr=Haber.objects.all().order_by("-toplamBegenme")[:6]
    guncelHaberler=Haber.objects.all().order_by("-id")[:5]
    liste=list()    
    for i in haberlerr:
        kontrol=AddFavoriHaber.objects.filter(haber=i).first()
        if kontrol is not None:
            liste.append(str(AddFavoriHaber.objects.filter(haber=i).count()))
        else:
            liste.append("0")
    liste2=list()
    for i in haberlerr:
        kontrol=YorumHaber.objects.filter(yorumHaber=i).first()
        if kontrol is not None:
            liste2.append(str(YorumHaber.objects.filter(yorumHaber=i).count()))
        else:
            liste2.append("0")
    zipp=zip(haberlerr, liste, liste2)     
    paylasimlargüncel=Forum.objects.all().order_by("-BegenmeSayısı")[:5]
    if request.user.is_authenticated:
        arkadaslar=AddMyFriends.objects.filter(ekleyen=request.user).values("eklenen")
        arkadaslarr=User.objects.filter(id__in=arkadaslar).order_by("-last_login")
    else:
        arkadaslarr="Giriş Yapılmamış"
    context={
        "oyunlar":oyun,
        "oyunlar_active":oyun_active,
        "haberlerr":zipp,
        "paylasimlargüncel":paylasimlargüncel,
        "arkadaslar":arkadaslarr,
    }
    return render(request,"anaSayfa.html", context)