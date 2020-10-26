DJANGO PROJESİ

Bu proje de oyuncuların, oyunlar hakkında forum da konuşabileceği, birbirlerini arkadaş ekleyip oyun arkadaşı edineceği, moderetörlerin yazdığı haberleri okuyabileceği bir proje.

#### Ana Sayfa

Sayfanın en üstünde oyunlardan alınan 3 tane gastgele oyun ile slideshow yaptım. Haberleri en çok beğeni alan 6 haberi ana sayfaya koydum. Forumları ise en güncel olarak sıraladım. Eğer ki kullanıcı giriş yaptı ise arkadaşlarının son giriş tarihine göre sıraladım.  

![AnaSayfa](https://user-images.githubusercontent.com/61551987/97159541-1a5b8d80-178c-11eb-8c27-d0f5a0752f88.JPG)

#### Kayıt Ol

Djangonun hazır user modeli ile kullanarak kayıt ol sayfasını oluşturdum.

![Kayıt Ol](https://user-images.githubusercontent.com/61551987/97160693-c651a880-178d-11eb-9a40-3b514735cdaf.JPG)

#### Giriş Yap

Hazır olan user modelini veri tabanını ile sorgulayıp girişi sağladım.

![Giriş Yap](https://user-images.githubusercontent.com/61551987/97161013-4415b400-178e-11eb-9021-033255f8ce69.JPG)

#### Oyunlar

Oyunların hangi platformlar da oynandığını boolean field ile oluşturdum ve bunları bu şekilde ayırdım. Kategorileri charfield ile oluşturup sorgu işlemini icontains ile yaptım. Her oyun sırasının sonun da bir buton ekleyerek eğer kullanıcı giriş yaptı ise kendi listesine almasına olanak sağladım. 
![Oyunlar](https://user-images.githubusercontent.com/61551987/97161279-a5d61e00-178e-11eb-9226-72e13b8bb04e.JPG)

#### Haberler

Moderetorlerin yazdığı haberleri sıralıyorum. Kategoriler oyunlar kategorosin de olduğu gibi icontains ile yaptım. 

![Haberler](https://user-images.githubusercontent.com/61551987/97183322-b1d1d800-17ae-11eb-8e0c-e640788f6475.JPG)

#### Detail Haber

Sayfa da haberi yazan moderetör ile ilgili bir bölümde önceden yazdığı haberler ve hakkında kısmı yer alıoyor. Eğer kullanıcı giriş yaptı ise yorum yapabiliyor, haberi beğenebiliyor ve isterse haberi rapor edebiliyor. 

![Detail Haber](https://user-images.githubusercontent.com/61551987/97183881-56541a00-17af-11eb-8aa7-8e8d05c01b6f.JPG)

#### Haber Ekle

Haber eklemeyi /haberler/addHaber/ den yapıyorum content kısmını djongo ckeditor ile yaptım bu şekilde video ve görsel paylaşabildim. Forum ekle kısmı da aynı şekil de yaptım. 

![Haber Ekle](https://user-images.githubusercontent.com/61551987/97184632-2c4f2780-17b0-11eb-9e26-6d1f31c9ed3f.JPG)

#### Forum 

Kullanıcılar giriş yaptı ise forum da yazı yazabilirler, yorum bırakabilirler, beğenebilirler veya rapor edebilirler. 

![forum](https://user-images.githubusercontent.com/61551987/97185289-ec3c7480-17b0-11eb-9c87-68bd44fa85e4.JPG)

#### Profil 

Her kayıt olan kullanıcın otomatik profil modeli oluşturuluyor. Bu şekilde user modelini değiştirmeden user modeline profil modelini bağlayıp bu şekilde kullanmayı seçtim. Buradan oyunlarımdan daha önce seçtiği oyunlara ulaşabilir ve listesinde olan oyunun hangi arkadaşında da listesinde olduğunu görebilir. Kullanıcın blokladığı kullanıcıları buradan görebilir ve bloğu buradan kaldırabilir. Kullanıcın blokladığı user, bloklayen kullanıcın profilini göremez ayrıca bloklayan kullanıcı bloklanan kullanıcının yazdığı forumlar /forum/ da gözükmez. 

![Profil](https://user-images.githubusercontent.com/61551987/97185729-797fc900-17b1-11eb-8d0c-7cca1a5c19ee.JPG)

#### Arkadas Bul

Kullanıcıları buradan bulabiliriz listenen kullanıcıların ortak oyunları ve ortak arkadaslarını görebilriz.
![Arkadas Bul](https://user-images.githubusercontent.com/61551987/97186930-f9f2f980-17b2-11eb-9740-982af7a26768.JPG)
