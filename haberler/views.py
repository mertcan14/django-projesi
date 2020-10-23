from django.shortcuts import render, redirect, get_object_or_404
from haberler.forms import addhaberForm, addyorumForm, addreportForm
from django.contrib import messages
from haberler.models import Haber, YorumHaber, LikeYorumHaber, AddFavoriHaber, AddReportHaber
from django.contrib.auth.decorators import login_required

def userNotLogged(func):
    def _func(request, *args, **kwargs):
        # eğer bir kullanıcımız giriş yapmış ise
        if request.user.is_authenticated:
            # Anasayfaya yönlendiriyoruz
            return func(request, *args, **kwargs)      
        #giris yapmamışsa fonksiyonu olduğu gibi dönderiyoruz ve sayfaya erişiyor
        messages.error(request,"Maalesef üye değilsiniz")
        return redirect("kayit")
    return _func


def haberler(request):
    keyword=request.GET.get("keyword_haber")
    if keyword is not None:
        haberlerr=Haber.objects.filter(baslik__icontains=keyword)
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
        context={
            "haberlerr":zipp,
            "guncelHaberler":guncelHaberler
        }
        return render(request,"haberler.html",context)
    haberlerr=Haber.objects.all().order_by("-toplamBegenme")
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
    context={
        "haberlerr":zipp,
        "guncelHaberler":guncelHaberler,
    }
    return render(request,"haberler.html",context)

def addHaber(request):
    if request.method=="POST":
        form=addhaberForm(request.POST, request.FILES)
        if form.is_valid():
            haber= form.save(commit=False)
            haber.user=request.user
            haber.save()
            newFav=AddFavoriHaber()
            newFav.haber=haber
            newFav.user=haber.user
            newFav.toplam=str(haber.user.id)+str(haber.id)
            newFav.save()
            haber.toplamBegenme=str(AddFavoriHaber.objects.filter(haber=haber.id).count())
            haber.save()
            messages.success(request,"Başarı ile eklendi")
            return redirect("anaSayfa")
        else:
            form=addhaberForm(request.POST, request.FILES)
            context={
                "form":form
            }
            return render(request,"addHaber.html", context)
    
    else:
        form=addhaberForm()
        context={
            "form":form
        }
        return render(request,"addHaber.html", context)

def haberlerTag(request, tag):
    keyword=request.GET.get("keyword_haber")
    if keyword is not None:
        haberlerr=Haber.objects.filter(baslik__icontains=keyword).filter(tags__icontains=tag)
        guncelHaberler=Haber.objects.all().order_by("-id")[:5]
        liste=list()    
        for i in haberlerr:
            kontrol=AddFavoriHaber.objects.filter(haber=i).first()
            if kontrol is not None:
                liste.append(str(AddFavoriHaber.objects.filter(haber=i).count()))
            else:
                liste.append("0")
        zipp=zip(haberlerr, liste)
        context={
            "haberlerr":zipp,
            "guncelHaberler":guncelHaberler
        }
        return render(request,"haberler.html",context)
    haberlerr=Haber.objects.filter(tags__icontains=tag)
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
    context={
        "haberlerr":zipp,
        "guncelHaberler":guncelHaberler,
    }
    return render(request,"haberler.html",context)

def haberlerDetail(request, id):
    if request.method=="POST":
        form=addyorumForm(request.POST)
        try:
            if form.is_valid():
                formm=form.save(commit=False)
                formm.yorumYapan=request.user
                formm.yorumHaber=Haber.objects.filter(id=id).first()
                formm.save()
                haberr=get_object_or_404(Haber, id=id)
                sayı=haberr.toplamYorum
                sayı= int(sayı)+1
                haberr.toplamYorum=str(sayı)
                haberr.save()
                messages.success(request,"Başarı ile eklendi.")
                return redirect("/haberler/detail/"+str(id))
        except:
            messages.info(request,"Hata Alındı")
            return redirect("/haberler/detail/"+str(id))
    else:
        haberlerr=Haber.objects.filter(id=id).first()
        yazarguncel=Haber.objects.filter(user=haberlerr.user).exclude(id=haberlerr.id).order_by("-id")[:5]
        yorumlarHaber=YorumHaber.objects.filter(yorumHaber=id)
        liste=list()
        for i in yorumlarHaber:
            liste.append(LikeYorumHaber.objects.filter(yorum=i.id).count())
        zipp=zip(yorumlarHaber, liste)
        form=addyorumForm()
        reportform=addreportForm()
        context={
            "haberler":haberlerr,
            "yazarguncel":yazarguncel,
            "yorumlarHaber":zipp,
            "form":form,
            "reportform":reportform,
        }
        return render(request,"detailHaber.html", context)
@login_required
def likeYorumHaber(request, id):
    yorum=get_object_or_404(YorumHaber, id=id)
    try:
        kontrol=str(yorum.id)+str(request.user.id)
        kontrolyorum=LikeYorumHaber.objects.filter(toplam=kontrol).first()
        if kontrolyorum is None:
            newLike=LikeYorumHaber()
            newLike.yorum=yorum
            newLike.yorumbegenen=request.user
            newLike.toplam=kontrol
            newLike.save()
            messages.success(request,"Beğenildi")
            return redirect("/haberler/detail/"+str(yorum.yorumHaber.id))
        else:
            messages.info(request,"Beğenmekten vazgeçildi")
            kontrolyorum.delete()
            return redirect("/haberler/detail/"+str(yorum.yorumHaber.id))
    except:
        messages.info(request, "Hata Alındı.")
        return redirect("/haberler/detail/"+str(yorum.yorumHaber.id))

@userNotLogged
def addFavoriHaber(request, id):
    haber=get_object_or_404(Haber, id=id)
    if haber is not None:      
        kontrol=str(request.user.id)+str(id)
        kontrolHaber=AddFavoriHaber.objects.filter(toplam=kontrol).first()
        if kontrolHaber is None:
            newFav=AddFavoriHaber()
            newFav.haber=haber
            newFav.user=request.user
            newFav.toplam=kontrol
            newFav.save()
            sayı = haber.toplamBegenme
            sayı = int(sayı)+1
            haber.toplamBegenme=str(sayı)
            haber.save()
            messages.success(request,"Başarı ile beğenildi.")
            return redirect("/haberler/detail/"+str(id))
        else:
            messages.info(request,"Beğenmekten Vazgeçildi.")
            sayı = haber.toplamBegenme
            sayı = int(sayı)-1
            haber.toplamBegenme=str(sayı)
            haber.save()
            kontrolHaber.delete()
            return redirect("/haberler/detail/"+str(id))

@login_required
def addReportHaber(request, id):
    form=addreportForm(request.POST)
    try:
        formm=form.save(commit=False)
        formm.user=request.user
        formm.haber=get_object_or_404(Haber, id=id)
        kontrol=str(request.user.id)+str(id)
        kontrolrep=AddReportHaber.objects.filter(toplam=kontrol).first()
        if kontrolrep is not None:
            messages.warning(request,"Önceden reportlamışsınız..")
            return redirect("/haberler/detail/"+str(id))
        formm.toplam=kontrol
        formm.save()
        messages.success(request,"Başarı ile iletildi..")
        return redirect("/haberler/detail/"+str(id))
    except:
        messages.warning(request,"Hata Alındı..")
        return redirect("/haberler/detail/"+str(id))

def haberlersıra(request, sıra):
    if sıra=="begen":
        keyword=request.GET.get("keyword_haber")
        if keyword is not None:
            haberlerr=Haber.objects.filter(baslik__icontains=keyword)
            guncelHaberler=Haber.objects.all().order_by("-id")[:5]
            liste=list()
            for i in haberlerr:
                kontrol=AddFavoriHaber.objects.filter(haber=i).first()
                if kontrol is not None:
                    liste.append(str(AddFavoriHaber.objects.filter(haber=i).count()))
                else:
                    liste.append("0")
            zipp=zip(haberlerr, liste)
            context={
                "haberlerr":zipp,
                "guncelHaberler":guncelHaberler
            }
            return render(request,"haberler.html",context)
        haberlerr=Haber.objects.all().order_by("-toplamBegenme", "-toplamYorum")
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
        context={
            "haberlerr":zipp,
            "guncelHaberler":guncelHaberler,
        }
        return render(request,"haberler.html",context)
    elif sıra=="guncel":
        keyword=request.GET.get("keyword_haber")
        if keyword is not None:
            haberlerr=Haber.objects.filter(baslik__icontains=keyword)
            guncelHaberler=Haber.objects.all().order_by("-id")[:5]
            liste=list()
            for i in haberlerr:
                kontrol=AddFavoriHaber.objects.filter(haber=i).first()
                if kontrol is not None:
                    liste.append(str(AddFavoriHaber.objects.filter(haber=i).count()))
                else:
                    liste.append("0")
            zipp=zip(haberlerr, liste)
            context={
                "haberlerr":zipp,
                "guncelHaberler":guncelHaberler
            }
            return render(request,"haberler.html",context)
        haberlerr=Haber.objects.all().order_by("-id")
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
        context={
            "haberlerr":zipp,
            "guncelHaberler":guncelHaberler,
        }
        return render(request,"haberler.html",context)
    else:
        keyword=request.GET.get("keyword_haber")
        if keyword is not None:
            haberlerr=Haber.objects.filter(baslik__icontains=keyword)
            guncelHaberler=Haber.objects.all().order_by("-id")[:5]
            liste=list()
            for i in haberlerr:
                kontrol=AddFavoriHaber.objects.filter(haber=i).first()
                if kontrol is not None:
                    liste.append(str(AddFavoriHaber.objects.filter(haber=i).count()))
                else:
                    liste.append("0")
            zipp=zip(haberlerr, liste)
            context={
                "haberlerr":zipp,
                "guncelHaberler":guncelHaberler
            }
            return render(request,"haberler.html",context)
        haberlerr=Haber.objects.all().order_by("-toplamYorum", "-toplamBegenme")
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
        context={
            "haberlerr":zipp,
            "guncelHaberler":guncelHaberler,
        }
        return render(request,"haberler.html",context)
# Create your views here.
