from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import addforumForm, addYorumForm, addReportForm
from django.contrib import messages
from .models import Forum, Yorumforum, LikeYorum, LikeForum, ReportForum
from user.models import BlockMyFriends

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


def forum(request):
    if request.user.is_authenticated:
        keyword= request.GET.get("keyword_forum")

        if keyword:
            engellenenler= BlockMyFriends.objects.filter(bloklayan= request.user).values('bloklanan')
            paylasimlar=Forum.objects.exclude(soran_id__in =engellenenler).filter(title__icontains= keyword)[::-1]
            paylasimlargüncel=Forum.objects.exclude(soran_id__in =engellenenler).order_by("-BegenmeSayısı")[:8]
            yorum=list()
            begeni=list()
            for i in paylasimlar:
                kontrol=Yorumforum.objects.filter(yorumForm=i.id).first()
                kontrolBegeni=LikeForum.objects.filter(like=i.id).first()
                if kontrol is not None:
                    yorum.append(str(Yorumforum.objects.filter(yorumForm=i.id).count()))
                if kontrol is None:
                    yorum.append("0")
                if kontrolBegeni is not None:
                    begeni.append(str(LikeForum.objects.filter(like=i.id).count()))
                if kontrolBegeni is None:
                    begeni.append("0")
                
            zipp=zip(paylasimlar, yorum, begeni)
            context={
            "paylasimlar":zipp,
            "paylasimlargüncel":paylasimlargüncel
            }
            return render(request,"forum.html", context)
        engellenenler= BlockMyFriends.objects.filter(bloklayan= request.user).values('bloklanan')
        paylasimlar=Forum.objects.exclude(soran_id__in =engellenenler)[::-1]
        paylasimlargüncel=Forum.objects.exclude(soran_id__in =engellenenler).order_by("-BegenmeSayısı")[:8]
        yorum=list()
        begeni=list()
        for i in paylasimlar:
            kontrol=Yorumforum.objects.filter(yorumForm=i.id).first()
            kontrolBegeni=LikeForum.objects.filter(like=i.id).first()
            if kontrol is not None:
                yorum.append(str(Yorumforum.objects.filter(yorumForm=i.id).count()))
            if kontrol is None:
                yorum.append("0")
            if kontrolBegeni is not None:
                begeni.append(str(LikeForum.objects.filter(like=i.id).count()))
            if kontrolBegeni is None:
                begeni.append("0")
            

        zipp=zip(paylasimlar, yorum, begeni)
        context={
            "paylasimlar":zipp,
            "paylasimlargüncel":paylasimlargüncel
        }
        return render(request,"forum.html",context)
    else:
        keyword= request.GET.get("keyword_forum")

        if keyword:
            paylasimlar=Forum.objects.filter(title__icontains= keyword)[::-1]
            paylasimlargüncel=Forum.objects.all()[::-1]
            yorum=list()
            begeni=list()
            for i in paylasimlar:
                kontrol=Yorumforum.objects.filter(yorumForm=i.id).first()
                kontrolBegeni=LikeForum.objects.filter(like=i.id).first()
                if kontrol is not None:
                    yorum.append(str(Yorumforum.objects.filter(yorumForm=i.id).count()))
                if kontrol is None:
                    yorum.append("0")
                if kontrolBegeni is not None:
                    begeni.append(str(LikeForum.objects.filter(like=i.id).count()))
                if kontrolBegeni is None:
                    begeni.append("0")
                

            zipp=zip(paylasimlar, yorum, begeni)
            context={
            "paylasimlar":zipp,
            "paylasimlargüncel":paylasimlargüncel
            }
            return render(request,"forum.html", context)
        paylasimlar=Forum.objects.all()[::-1]
        paylasimlargüncel=Forum.objects.all().order_by("-BegenmeSayısı")
        yorum=list()
        begeni=list()
        for i in paylasimlar:
            kontrol=Yorumforum.objects.filter(yorumForm=i.id).first()
            kontrolBegeni=LikeForum.objects.filter(like=i.id).first()
            if kontrol is not None:
                yorum.append(str(Yorumforum.objects.filter(yorumForm=i.id).count()))
            if kontrol is None:
                yorum.append("0")
            if kontrolBegeni is not None:
                begeni.append(str(LikeForum.objects.filter(like=i.id).count()))
            if kontrolBegeni is None:
                begeni.append("0")
            

        zipp=zip(paylasimlar, yorum, begeni)
        context={
            "paylasimlar": zipp,
            "paylasimlargüncel":paylasimlargüncel
        }
        return render(request, "forum.html", context)

@userNotLogged
def addForum(request):
    if request.method == "POST":
        form=addforumForm(request.POST)
        if form.is_valid():
            
            formm=form.save(commit=False)
            formm.soran=request.user
            formm.save()
            messages.success(request,"Başarı ile eklendi.")
            return redirect("forum")
        else:
            form=addforumForm(request.POST)
            context={
                "form":form
            }
            return render(request,"addForum.html",context)
    else:
        form=addforumForm()
        context={
            "form":form
        }
        return render(request,"addForum.html", context)
    
def viewForum(request, id):
    
    if request.method=="POST":
        form=addYorumForm(request.POST)
        formreport=addReportForm()
        try:
            if form.is_valid():
                formm=form.save(commit=False)
                formm.yorumYapan=request.user
                formm.yorumForm=Forum.objects.filter(id=id).first()
                formm.save()
                kontrol=Forum.objects.filter(id=id).first()
                sayı=kontrol.YorumSayısı
                sayı=int(sayı)+1
                kontrol.YorumSayısı=sayı
                kontrol.save()
                messages.success(request,"Yorum eklendi.")
            formbos=addYorumForm()
            soru=get_object_or_404(Forum, id=id)
            yazar=Forum.objects.filter(soran_id= soru.soran_id)[:5:-1]
            yorumlar=Yorumforum.objects.filter(yorumForm=id)
            liste=list()
            listekisi=list()
            for yorumm in Yorumforum.objects.filter(yorumForm=id):
                liste.append(LikeYorum.objects.filter(yorum=yorumm).count())
                if yorumm.yorumYapan == request.user:
                    listekisi.append(1)
                else:
                    listekisi.append(0)
            zipp=zip(yorumlar, liste,listekisi)
            toplamBegenme=LikeForum.objects.filter(like=id).count()
            toplamYorum=Yorumforum.objects.filter(yorumForm_id=id).count()
            context={
                "soru":soru,
                "yazar": yazar,
                "form":formbos,
                "formreport":formreport,
                "yorumlar":zipp,
                "toplamBegenme":toplamBegenme,
                "toplamYorum":toplamYorum
            }
            return render(request,"detailforum.html", context)
        except:
            messages.info(request,"Mallesef forum bulunamadı.")
            return redirect("/forum")
    else:
        form=addYorumForm()
        formreport=addReportForm()
        try:
            soru=get_object_or_404(Forum, id=id)
            yazar=Forum.objects.filter(soran_id= soru.soran_id)[:5:-1]
            yorumlar=Yorumforum.objects.filter(yorumForm=id)
            liste=list()
            listekisi=list()
            for yorumm in Yorumforum.objects.filter(yorumForm=id):
                liste.append(LikeYorum.objects.filter(yorum=yorumm).count())
                if yorumm.yorumYapan == request.user:
                    listekisi.append(1)
                else:
                    listekisi.append(0)
            zipp=zip(yorumlar, liste,listekisi)
            toplamBegenme=LikeForum.objects.filter(like=id).count()
            toplamYorum=Yorumforum.objects.filter(yorumForm_id=id).count()
            context={
                "soru":soru,
                "yazar": yazar,
                "form":form,
                "formreport":formreport,
                "yorumlar":zipp,
                "toplamBegenme":toplamBegenme,
                "toplamYorum":toplamYorum
            }
            return render(request,"detailforum.html", context)
        except:
            messages.info(request,"Mallesef forum bulunamadı.")
            return redirect("/forum")


@userNotLogged
def likeYorum(request, id):
    yorum=get_object_or_404(Yorumforum, id=id)
    try:
        kontrol=str(yorum.id)+ str(request.user.id)
        kontrolyorumbegenen=LikeYorum.objects.filter(toplam=kontrol).first()
        if kontrolyorumbegenen is None:
            newLike=LikeYorum()
            newLike.yorumbegenen=request.user
            newLike.yorum= yorum
            newLike.toplam= str(yorum.id)+ str(request.user.id)
            newLike.save()
            messages.success(request,"Beğenildi")
            return redirect("/forum/detail/"+str(yorum.yorumForm.id))
        else:
            messages.info(request,"Beğenmekten vazgeçildi")
            kontrolyorumbegenen.delete()
            return redirect("/forum/detail/"+str(yorum.yorumForm.id))
    except:
        messages.info(request, "Hata Alındı.")
        return redirect("/forum/detail/"+str(yorum.yorumForm.id))

@userNotLogged
def likeForum(request, id):
    kontrol=get_object_or_404(Forum, id=id)
    kontrolLike=str(request.user)+ str(id)
    like=LikeForum.objects.filter(toplam=kontrolLike).first()
    if like is None:
        try:    
            newLike=LikeForum()
            newLike.begenen=request.user
            newLike.like=kontrol
            newLike.toplam=kontrolLike
            newLike.save()
            sayı=kontrol.BegenmeSayısı
            sayı=int(sayı)+1
            kontrol.BegenmeSayısı=str(sayı)
            kontrol.save()
            messages.success(request,"Başarı ile beğenildi.")
            return redirect("/forum/detail/"+str(id))
        except:
            messages.info(request,"Hata alındı.")
            return redirect("/forum/detail/"+str(id))
    else:
        like.delete()
        sayı=kontrol.BegenmeSayısı
        sayı=int(sayı)-1
        kontrol.BegenmeSayısı=str(sayı)
        kontrol.save()
        messages.warning(request,"Beğeni silindi.")
        return redirect("/forum/detail/"+str(id))

@login_required
def deleteYorum(request,id):
    kontrol=get_object_or_404(Yorumforum, id=id)
    forumm=Forum.objects.filter(id=kontrol.yorumForm.id).first()
    if request.user==kontrol.yorumYapan:
        kontrol.delete()
        sayı=forumm.YorumSayısı
        sayı=int(sayı)-1
        forumm.YorumSayısı=sayı
        forumm.save()
        messages.success(request,"Başarı ile silindi")
        return redirect("/forum/detail/"+str(forumm.id))
    else:
        messages.warning(request,"Erişime izniniz yok.")
        return redirect("/forum")

@userNotLogged
def reportForum(request,id):
    try:
        kontrol=str(request.user.id)+str(id)
        kontrolforum=ReportForum.objects.filter(toplam=kontrol).first()
        form=addReportForm(request.POST)
        if kontrolforum is None:
            formm=form.save(commit=False)
            formm.report=get_object_or_404(Forum, id=id)
            formm.reportlayan=request.user
            formm.toplam=kontrol
            formm.save()
            messages.success(request,"Başarı ile iletildi...")
            return redirect("/forum/detail/"+str(id))
        else:
            messages.info(request,"Önceden rapor edilmiş...")
            return redirect("/forum/detail/"+str(id))
    except:
        messages.info(request,"Hata Alındı...")
        return redirect("/forum/detail/"+str(id))