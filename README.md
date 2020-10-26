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

#### Giriş Yap

Oyunların hangi platformlar da oynandığını boolean field ile oluşturdum ve bunları bu şekilde ayırdım. Kategorileri charfield ile oluşturup sorgu işlemini icontains ile yaptım. Her oyun sırasının sonun da bir buton ekleyerek eğer kullanıcı giriş yaptı ise kendi listesine almasına olanak sağladım. 
![Oyunlar](https://user-images.githubusercontent.com/61551987/97161279-a5d61e00-178e-11eb-9226-72e13b8bb04e.JPG)
