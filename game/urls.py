from django.urls import path, include
from game import views
urlpatterns = [
    path("", views.oyunlar, name="oyun"),
    path("aksiyon/", views.aksiyonOyunlar,name="aksiyonOyunlar"),
    path("macera/", views.maceraOyunlar,name="maceraOyunlar"),
    path("fps/", views.fpsOyunlar,name="fpsOyunlar"),
    path("yaris/", views.yarısOyunlar,name="yarısOyunlar"),
    path("hayattakalma/", views.hayattakalmaOyunlar,name="yarısOyunlar"),
    path("spor/", views.sporOyunlar,name="yarısOyunlar"),
    path("strateji/", views.stratejiOyunlar,name="stratejiOyunlar"),
    path("deneme/<int:id>",views.deneme, name="deneme"),
    path("add/", views.addoyun, name="addoyun"),
    path("detail/<str:isim>", views.oyundetail, name="oyundetail"),
    path("pcoyunlar/", views.pcOyunlar, name="pcoyunlar"),
    path("mobiloyunlar/", views.mobilOyunlar, name="mobiloyunlar"),
    path("konsoloyunlar/", views.konsolOyunlar, name="konsoloyunlar"),
    path("detail/add/<int:id>", views.addmygame, name="addmygame"),
    path("detail/delete/<int:id>", views.deletemygame, name="deletemygame"),
]