from django.contrib import admin
from django.urls import path, include
from my_game_friends import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.anasayfa, name="anaSayfa"),
    path('user/', include('user.urls')),
    path('oyunlar/', include('game.urls')),
    path('forum/', include('forum.urls')),
    path('haberler/', include('haberler.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
