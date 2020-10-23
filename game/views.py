from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from game.forms import addGameForm
from game.models import Oyunlar
from user.models import Mygame
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
def userNotLogged(func):
    def _func(request, *args, **kwargs):
        # eğer bir kullanıcımız giriş yapmış ise
        if request.user.is_staff:
            # Anasayfaya yönlendiriyoruz
            return func(request, *args, **kwargs)      
        #giris yapmamışsa fonksiyonu olduğu gibi dönderiyoruz ve sayfaya erişiyor
        messages.error(request,"Maalesef erişim izniniz yok")
        return redirect("anaSayfa")
    return _func

def userNotLogged2(func):
    def _func(request, *args, **kwargs):
        # eğer bir kullanıcımız giriş yapmış ise
        if request.user.is_authenticated:
            # Anasayfaya yönlendiriyoruz
            return func(request, *args, **kwargs)      
        #giris yapmamışsa fonksiyonu olduğu gibi dönderiyoruz ve sayfaya erişiyor
        messages.error(request,"Maalesef üye değilsiniz")
        return redirect("kayit")
    return _func

def oyunlar(request):
    keyword= request.GET.get("keyword")

    if keyword:
        oyun=Oyunlar.objects.filter(oyun_isim__icontains= keyword)
        return render(request,"oyunlar.html", {"oyun":oyun})
    oyun=Oyunlar.objects.all()
    context={
        "oyun":oyun,
    }
    return render(request, "oyunlar.html",context)

def aksiyonOyunlar(request):
    oyunlar=Oyunlar.objects.filter(kategoriler__icontains= "aksiyon")
    context={
        "oyun":oyunlar
    }
    return render(request,"aksiyonoyunlar.html", context)

def stratejiOyunlar(request):
    oyunlar=Oyunlar.objects.filter(kategoriler__icontains= "strateji")
    context={
        "oyun":oyunlar
    }
    return render(request,"aksiyonoyunlar.html", context)

def maceraOyunlar(request):
    oyunlar=Oyunlar.objects.filter(kategoriler__icontains= "macera")
    context={
        "oyun":oyunlar
    }
    return render(request,"aksiyonoyunlar.html", context)

def fpsOyunlar(request):
    oyunlar=Oyunlar.objects.filter(kategoriler__icontains= "fps")
    context={
        "oyun":oyunlar
    }
    return render(request,"aksiyonoyunlar.html", context)

def yarısOyunlar(request):
    oyunlar=Oyunlar.objects.filter(kategoriler__icontains= "yarış")
    context={
        "oyun":oyunlar
    }
    return render(request,"aksiyonoyunlar.html", context)

def sporOyunlar(request):
    oyunlar=Oyunlar.objects.filter(kategoriler__icontains= "spor")
    context={
        "oyun":oyunlar
    }
    return render(request,"aksiyonoyunlar.html", context)

def hayattakalmaOyunlar(request):
    oyunlar=Oyunlar.objects.filter(kategoriler__icontains= "hayatta kalma")
    context={
        "oyun":oyunlar
    }
    return render(request,"aksiyonoyunlar.html", context)

@userNotLogged
def addoyun(request):
    if request.method=="POST":
        form=addGameForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Başarı ile eklendi")
            return redirect("anaSayfa")
        else:
            form=addGameForm(request.POST, request.FILES)
            context={
                "form":form
            }
            return render(request,"addGame.html", context)
    
    else:
        form=addGameForm()
        context={
            "form":form
        }
        return render(request,"addGame.html", context)

def oyundetail(request, isim):
    oyun=get_object_or_404(Oyunlar, oyun_isim=isim)
    if oyun is not None:
        platform=str()
        if oyun.bilgisayar_platform== True:
            bSayı= 1
            platform += str(bSayı)
        if oyun.mobil_platform== True:
            mSayı= 2
            platform += str(mSayı)
        if oyun.konsol_platform== True:
            kSayı= 3
            platform += str(kSayı)
        context={
            "oyun": oyun,
            "platform": platform
        }
        return render(request,"detailoyun2.html", context)
    else:
        return redirect("kayit")
    
def pcOyunlar(request):
    keyword= request.GET.get("keyword")

    if keyword:
        oyun=Oyunlar.objects.filter(oyun_isim__icontains= keyword, bilgisayar_platform= True)
        return render(request,"pcoyunlar.html", {"oyun":oyun})
    oyun=Oyunlar.objects.filter(bilgisayar_platform= True)
    context={
        "oyun":oyun
    }
    return render(request,"pcoyunlar.html", context)

def mobilOyunlar(request):
    keyword= request.GET.get("keyword")

    if keyword:
        oyun=Oyunlar.objects.filter(oyun_isim__icontains= keyword, mobil_platform= True)
        return render(request,"mobiloyunlar.html", {"oyun":oyun})
    oyun=Oyunlar.objects.filter(mobil_platform= True)
    context={
        "oyun":oyun
    }
    return render(request,"mobiloyunlar.html", context)

def konsolOyunlar(request):
    keyword= request.GET.get("keyword")

    if keyword:
        oyun=Oyunlar.objects.filter(oyun_isim__icontains= keyword, konsol_platform= True)
        return render(request,"konsoloyunlar.html", {"oyun":oyun})
    oyun=Oyunlar.objects.filter(konsol_platform= True)
    context={
        "oyun":oyun
    }
    return render(request,"konsoloyunlar.html", context)

@userNotLogged2
def addmygame(request,id):
    oyun= Oyunlar.objects.filter(id= id).first()
    if oyun is not None:
        try:
            ekle= Mygame()
            ekle.user=request.user
            ekle.game=oyun
            ekle.toplam= str(request.user.id)+str(oyun.id)
            ekle.save()
        except IntegrityError:
            messages.info(request,"Zaten eklenmiş durumda")
        return redirect("/oyunlar/detail/"+str(oyun.oyun_isim))
    else:
        messages.info(request,"Oyun Bulunamadı")
        return redirect("oyun")

@userNotLogged2
def deletemygame(request,id):
    oyun=Mygame.objects.filter(user=request.user, game=id).first()
    oyun.delete()
    messages.success(request,"Başarı ile silindi.")
    return redirect("listmygame")

def deneme(request,id):
    oyun=get_object_or_404(Oyunlar, id=id)
    if oyun is not None:
        platform=str()
        if oyun.bilgisayar_platform== True:
            bSayı= 1
            platform += str(bSayı)
        if oyun.mobil_platform== True:
            mSayı= 2
            platform += str(mSayı)
        if oyun.konsol_platform== True:
            kSayı= 3
            platform += str(kSayı)
        context={
            "oyun": oyun,
            "platform": platform
        }
        return render(request,"detailoyun2.html", context)
    else:
        return redirect("kayit")
