from django.urls import path, include
from haberler import views
urlpatterns = [
    path('', views.haberler, name="haberler"),
    path('sırala/<str:sıra>', views.haberlersıra, name="haberlersıra"),
    path('detail/<int:id>', views.haberlerDetail, name="haberlerDetail"),
    path('detail/add-favori/<int:id>', views.addFavoriHaber, name="addFavoriHaber"),
    path('detail/add-report/<int:id>', views.addReportHaber, name="addReportHaber"),
    path('kategori/<str:tag>', views.haberlerTag, name="haberlerTag"),
    path('addHaber/', views.addHaber, name="addHaberler"),
    path('detail/favYorum/<int:id>', views.likeYorumHaber, name="likeYorumHaber"),
]