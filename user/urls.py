from django.urls import path, include
from user import views


urlpatterns = [
    path("kayıt/", views.kayit, name="kayit"),
    path("logout/", views.logoutUser, name="logout"),
    path("giris/", views.usergiris, name="giris"),
    path("profil/", views.userProfil, name="profil"),
    path("find/friends/", views.findFriends, name="findFriends"),
    path("profil/mygame/", views.listmygame, name="listmygame"),
    path("profil/blockuser/", views.listblockuser, name="listblockuser"),
    path("profil/<int:id>", views.viewProfil, name="viewProfil"),
    path("profil/oyunlar/<int:id>", views.listgame, name="listgame"),
    path("profil/forum/<int:id>", views.listforum, name="listforum"),
    path("add/<int:id>", views.addFriends, name="addFriends"),
    path("block/<int:id>", views.blockFriends, name="blockFriends"),
    path("profil/blockuser/delete/<int:id>", views.deleteblockFriends, name="deleteblockFriends"),
    path("arkadas/delete/<int:id>", views.deleteaddFriends, name="deleteaddFriends"),
    path("arkadaslar/", views.arkadaslar, name="arkadaslar"),
    path("bildirim/", views.bildirim, name="bildirim"),
]