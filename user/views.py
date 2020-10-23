from django.shortcuts import render,redirect, get_object_or_404, HttpResponse
from user.forms import kayitForm,girisForm, updateProfileForms, updateUserForms
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from passlib.hash import sha256_crypt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from user.models import Profil, Mygame, AddMyFriends, BlockMyFriends
from game.models import Oyunlar
from django.db.utils import IntegrityError
from forum.models import Forum
def kayit(request):
    form = kayitForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            email=form.cleaned_data.get("email")
            newUser= User(username=username, email=email)
            newUser.set_password(password)
            newUser.save()
            login(request,newUser)
            messages.success(request,"Başarı ile kayıt olundu...")
            return redirect("anaSayfa")
        context={
            "form":form
        }
        return render(request,"kayit.html",context)

    else:
        form = kayitForm()
        context={
            "form":form
        }
        return render(request,"kayit.html", context)

def logoutUser(request):
    logout(request)
    messages.success(request,"Başarı ile çıkış yapıldı")
    return redirect("anaSayfa")

def usergiris(request):
    form=girisForm(request.POST or None)
    if request.method=="POST":
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            user=authenticate(username=username, password=password)
            if user is None:
                messages.warning(request,"Şifre veya kullanıcı adı hatalı.")
                return redirect("giris")
            login(request,user)
            messages.success(request,"Başarı ile girildi")
            return redirect("anaSayfa")
        return redirect("kayit")
    context={
        "form": form
    }    
    return render(request,"usergiris.html",context)

@login_required
def userProfil(request):
    if request.method == 'POST':
        user_form = updateUserForms(request.POST, request.FILES, instance=request.user)
        profil_form = updateProfileForms(request.POST, request.FILES , instance=request.user.profil)
        profil= Profil.objects.filter(user= request.user)
        if user_form.is_valid() and profil_form.is_valid():
            user_form.save()
            profil_form.save()
            messages.success(request,"başarı ile eklendi")
            return redirect("profil")
        return redirect("anaSayfa")
    
    else:
        user_form = updateUserForms(instance=request.user)
        profil_form = updateProfileForms(instance=request.user.profil)
        return render(request,"userProfil.html", {"user_form":user_form, "profil_form":profil_form})
@login_required
def listmygame(request):
    """if request.method=="POST":
        aranan=request.POST.get("aranan-oyun",None)
        try:
            oyun=Oyunlar.objects.filter(oyun_isim=aranan)
            html = ("<H1>%s</H1>", oyun)
        except:
            messages.info(request, "Mallesef bir sonuç bulunamadı.")
            return redirect("/user/profil/mygame/")
    else:
        oyunlar= Mygame.objects.filter(user=request.user)
        context={
            "oyunlar":oyunlar
        }
        return render(request,"listeOyunlarım.html", context)"""
    keyword= request.GET.get("keyword_oyunlarım")

    if keyword:
        oyun=Oyunlar.objects.filter(oyun_isim__icontains= keyword).values("id")
        oyunlar= Mygame.objects.filter(game__in=oyun, user=request.user)
        oyunlarr=Mygame.objects.filter(game__in=oyun, user=request.user).values("game")
        arkadaslarr=AddMyFriends.objects.filter(ekleyen=request.user).values("eklenen")
        liste=list()
        for i in oyunlarr:
            sayac=0
            for j in Mygame.objects.filter(user__in=arkadaslarr).values("game").distinct():
                if i==j:
                    sayac +=1
                    liste.append(Mygame.objects.filter(game=i["game"]).filter(user__in=arkadaslarr))
            if sayac==0:
                liste.append("bos")
        klasor=zip(oyunlar, liste)
        context={
            "zipp":klasor,
        }
        return render(request,"listeOyunlarım.html", context)
        """oyun=Oyunlar.objects.filter(oyun_isim__icontains= keyword)
        return render(request,"oyunlar.html", {"oyun":oyun})
    """
    oyunlar= Mygame.objects.filter(user=request.user)
    oyunlarr= Mygame.objects.filter(user=request.user).values("game")
    arkadaslarr=AddMyFriends.objects.filter(ekleyen=request.user).values("eklenen")
    liste=list()
    for i in oyunlarr:
        sayac=0
        for j in Mygame.objects.filter(user__in=arkadaslarr).values("game").distinct():
            if i==j:
                sayac +=1
                liste.append(Mygame.objects.filter(game=i["game"]).filter(user__in=arkadaslarr))
        if sayac==0:
            liste.append("bos")
    klasor=zip(oyunlar, liste)
    context={
        "zipp":klasor,
    }
    return render(request,"listeOyunlarım.html", context)

def viewProfil(request, id):
    if request.user.is_authenticated:
        bloklayanUser=User.objects.filter(id=id).first()
        kontrolblok=BlockMyFriends.objects.filter(bloklayan=bloklayanUser, bloklanan=request.user).first()
        if kontrolblok is None:
            try:
                oyuncu=get_object_or_404(User, id=id)
                oyunn=Mygame.objects.filter(user=oyuncu).values("game")
                oyun=Mygame.objects.filter(user=oyuncu)[:5]
                oyunlarım=Mygame.objects.filter(user=request.user, game__in=oyunn)[:5]
                formlar= Forum.objects.filter(soran_id=id)[:5]
                """liste=list()
                for ortak in oyunlarım:
                    for ortak1 in oyunn:
                        if ortak==ortak1:
                            ortakoyun=Oyunlar.objects.filter(id=ortak)"""
                
                "ortakoyun= Oyunlar.objects.filter(id__in=liste)"
                toplam_oyun=len(Mygame.objects.filter(user=oyuncu))
                toplam_form=len(Forum.objects.filter(soran_id=id))
            except:
                messages.info(request,"Maalesef Kullanıcı bulunamadı.")
                return redirect("anaSayfa")
            if oyun is not None:
                context={
                    "oyuncu": oyuncu,
                    "oyun":oyunlarım,
                    "toplamoyun":toplam_oyun,
                    "formlar":formlar,
                    "toplamform":toplam_form,
                }
            else:
                context={
                    "oyuncu": oyuncu,
                }
            return render(request,"arkadasprofil.html", context)
        else:
            messages.info(request, "Oyuncunun profilini göremezsiniz...")
            return redirect("anaSayfa")
    else:
        try:
            oyuncu=get_object_or_404(User, id=id)
            oyun=Mygame.objects.filter(user=oyuncu)[:5]
            toplam_oyun=len(Mygame.objects.filter(user=oyuncu))
            formlar= Forum.objects.filter(soran_id=id)
            toplam_form=len(Forum.objects.filter(soran_id=id))
            toplamArkadas=AddMyFriends.objects.filter(eklenen=oyuncu).count()
            if toplamArkadas is None:
                toplamArkadas="0"
        except:
            messages.info(request,"Maalesef Kullanıcı bulunamadı.")
            return redirect("anaSayfa")
        if oyun is not None:
            context={
                "oyuncu": oyuncu,
                "oyun":oyun,
                "toplamoyun":toplam_oyun,
                "formlar":formlar,
                "toplamform":toplam_form,
                "toplamArkadas":toplamArkadas,
            }
        else:
            context={
                "oyuncu": oyuncu,
                "toplamArkadas":toplamArkadas,
            }
        return render(request,"arkadasprofil.html", context)

@login_required
def addFriends(request, id):
    ekleyenn=User.objects.filter(id=request.user.id).first()
    eklenenn=User.objects.filter(id=id).first()
    blokluUser= BlockMyFriends.objects.filter(bloklayan=request.user).filter(bloklanan=id).values("bloklanan").first()
    if blokluUser is not None:
        messages.info(request,"Bloklanan kullanıcı ilk bloğu kaldırmanız gerekiyor.")
        return redirect("/user/profil/"+ str(eklenenn.id))
    if eklenenn == ekleyenn:
        messages.info(request,"Kendinizi ekleyemezsiniz.")
        return redirect("/user/profil/"+ str(eklenenn.id))
       
    try:
        newFriend=AddMyFriends()
        newFriend.eklenen=eklenenn
        newFriend.ekleyen=ekleyenn
        newFriend.toplam=str(ekleyenn.id)+str(eklenenn.id)
        newFriend.save()
        messages.success(request,"Başarı ile eklendi")
        return redirect("/user/profil/"+ str(eklenenn.id))
    except IntegrityError:
        messages.info(request,"Zaten arkdaşınız.")
        return redirect("/user/profil/"+ str(eklenenn.id))

@login_required
def blockFriends(request, id):
    bloklayann=User.objects.filter(id=request.user.id).first()
    bloklanann=User.objects.filter(id=id).first()
    myfriends=AddMyFriends.objects.filter(ekleyen=request.user).filter(eklenen=id).first()
    if myfriends is not None:
        messages.info(request,"Kullanıcı arkadaşınız ilk arkadaşlığı kaldırmanız gerekiyor.")
        return redirect("/user/profil/"+ str(bloklanann.id))
    if bloklanann==bloklayann:
        messages.info(request,"Kendinizi engelleyemezsiniz..")
        return redirect("/user/profil/"+str(bloklanann.id))
    try:
        newFriend=BlockMyFriends()
        newFriend.bloklayan=bloklayann
        newFriend.bloklanan=bloklanann
        newFriend.toplam=str(bloklayann.id)+str(bloklanann.id)
        newFriend.save()
        messages.success(request,"Başarı ile engellendi")
        return redirect("/user/profil/"+ str(bloklanann.id))
    except IntegrityError:
        messages.info(request,"Önceden engellenmiş.")
        return redirect("/user/profil/"+ str(bloklanann.id))
@login_required
def listblockuser(request):
    blockuser=BlockMyFriends.objects.filter(bloklayan=request.user)
    context={
        "blockuser":blockuser
    }
    return render(request,"listebloklanan.html", context)

@login_required
def deleteblockFriends(request, id):
    blockdelete=BlockMyFriends.objects.filter(bloklayan= request.user, bloklanan=id).first()
    blockdelete.delete()
    messages.success(request,"Başarı ile engel kaldırıldı.")
    return redirect("/user/profil/blockuser/")

@login_required
def arkadaslar(request):
    keyword= request.GET.get("keyword_arkadas")

    if keyword:
        arananoyuncu= User.objects.filter(username__icontains= keyword)
        aranan=AddMyFriends.objects.filter(eklenen__in=arananoyuncu).filter(ekleyen=request.user)
        arkadaslarliste=AddMyFriends.objects.filter(ekleyen=request.user).values("eklenen")
        arkadasOneri=User.objects.exclude(id__in= arkadaslarliste).exclude(id=request.user.id)[:10]
        sonoyunarkadas=Mygame.objects.filter(user__in=arkadaslarliste).order_by("-id")[:5]
        context={
            "arkadaslar":aranan,
            "arkadasoneri": arkadasOneri,
            "sonoyunarkadas":sonoyunarkadas,
        }
        return render(request,"arkadaslar.html", context)
    arkadaslar=AddMyFriends.objects.filter(ekleyen=request.user)
    arkadaslarliste=AddMyFriends.objects.filter(ekleyen=request.user).values("eklenen")
    bloklananuser=BlockMyFriends.objects.filter(bloklayan=request.user).values("bloklanan")
    arkadasOneri=User.objects.exclude(id__in= arkadaslarliste).exclude(id=request.user.id).exclude(id__in=bloklananuser).order_by("?")[:5]
    sonoyunarkadas=Mygame.objects.filter(user__in=arkadaslarliste).order_by("-id")[:5]
         
    context={
        "arkadaslar": arkadaslar,
        "arkadasoneri": arkadasOneri,
        "sonoyunarkadas":sonoyunarkadas,
    }
    return render(request,"arkadaslar.html", context)

@login_required
def deleteaddFriends(request, id):
    user=AddMyFriends.objects.filter(eklenen=id, ekleyen=request.user).first()
    user.delete()
    messages.success(request,"Başarı ile arkadaşlardan silindi.")
    return redirect("/user/arkadaslar")

def listgame(request,id):
    try:
        oyuncu=get_object_or_404(User, id=id)
        oyunn=Mygame.objects.filter(user=oyuncu).values("game")
        oyunlarım=Mygame.objects.filter(user=request.user, game__in=oyunn)
        oyunlarımm=Mygame.objects.filter(user=request.user, game__in=oyunn).values("game")
        oyunları=Mygame.objects.exclude(game__in=oyunlarımm).filter(user=oyuncu)
    except:
        messages.info(request,"Maalesef Kullanıcı bulunamadı.")
        return redirect("anaSayfa")
    context={
        "oyuncu":oyuncu,
        "oyun":oyunları,
        "oyunlarım":oyunlarım,
    }
    return render(request,"listeOyunları.html", context)

def listforum(request,id):
    try:
        oyuncu=get_object_or_404(User, id=id)
        forumlar=Forum.objects.filter(soran=id)
    except:
        messages.info(request,"Maalesef kullanıcı bulunamadı.")
        return redirect("anaSayfa")
    context={
        "oyuncu":oyuncu,
        "forumlar":forumlar
    }
    return render(request,"listeForumları.html", context)

@login_required
def findFriends(request):
    keyword= request.GET.get("keyword_bularkadas")

    if keyword:
        bloklananuser=BlockMyFriends.objects.filter(bloklayan=request.user).values("bloklanan")
        arananoyuncu= User.objects.filter(username__icontains= keyword).exclude(id=request.user.id).exclude(id__in=bloklananuser)
        oyunlarr= Mygame.objects.filter(user=request.user).values("game")
        arkadaslarliste=AddMyFriends.objects.filter(ekleyen=request.user).values("eklenen")
        liste=list()
        for i in arananoyuncu:
            sayac=0
            deger=Mygame.objects.filter(user=i).filter(game__in=oyunlarr)[:5]
            if deger is not None:
                liste.append(deger)
                sayac+=1
            if sayac==0:
                liste.append("bos")
        listeArkadas= list()
        ortakArkadaslar=AddMyFriends.objects.filter(ekleyen__in=arananoyuncu).values("eklenen")
        for i in arananoyuncu:
            sayac=0
            tırnak=0
            for j in ortakArkadaslar:
                ii=AddMyFriends.objects.filter(eklenen__in=arkadaslarliste).filter(ekleyen=i).values("eklenen").distinct()
                for k in ii:
                    if k==j:
                        sayac+=1
                        if sayac==len(ii):
                            listeArkadas.append(AddMyFriends.objects.filter(eklenen__in=arkadaslarliste).filter(ekleyen=i))
            if sayac==0:
                listeArkadas.append("bos")
        klasor=zip(arananoyuncu, liste, listeArkadas)
        context={
            "oyuncular":klasor,
        }
        return render(request,"findfriends.html", context)


    arkadaslarliste=AddMyFriends.objects.filter(ekleyen=request.user).values("eklenen")
    bloklananuser=BlockMyFriends.objects.filter(bloklayan=request.user).values("bloklanan")
    arkadasOneri=User.objects.exclude(id__in= arkadaslarliste).exclude(id=request.user.id).exclude(id__in=bloklananuser).order_by("?")
    oyunlarr= Mygame.objects.filter(user=request.user).values("game")
    liste=list()
    for i in arkadasOneri:
        sayac=0
        deger=Mygame.objects.filter(user=i).filter(game__in=oyunlarr)[:5]
        if deger is not None:
            liste.append(deger)
            sayac+=1
        if sayac==0:
            liste.append("bos")
    listeArkadas= list()
    ortakArkadaslar=AddMyFriends.objects.filter(ekleyen__in=arkadasOneri).values("eklenen")
    for i in arkadasOneri:
        sayac=0
        tırnak=0
        for j in ortakArkadaslar:
            ii=AddMyFriends.objects.filter(eklenen__in=arkadaslarliste).filter(ekleyen=i).values("eklenen").distinct()
            for k in ii:
                if k==j:
                    sayac+=1
                    if sayac==len(ii):
                        listeArkadas.append(AddMyFriends.objects.filter(eklenen__in=arkadaslarliste).filter(ekleyen=i))
        if sayac==0:
            listeArkadas.append("bos")
    klasor=zip(arkadasOneri, liste, listeArkadas)
    context={
        "oyuncular":klasor,
    }
    return render(request,"findfriends.html", context)

@login_required
def bildirim(request):
    kontrol=AddMyFriends.objects.filter(ekleyen=request.user).first()
    if kontrol is None:
        messages.info(request,"Arkadaşınız bulunmuyor.")
        return redirect("/user/find/friends/")
    else:
        arkadas=AddMyFriends.objects.filter(ekleyen=request.user).values("eklenen")
        addFriends=AddMyFriends.objects.filter(ekleyen__in=arkadas).order_by("-id")[:10]
        addGame=Mygame.objects.filter(user__in=arkadas).order_by("-id")[:18]
        context={
            "addFriends":addFriends,
            "addGame":addGame,
        }
        return render(request,"bildirim.html", context)