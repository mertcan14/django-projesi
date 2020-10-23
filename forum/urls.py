from django.urls import path, include
from forum import views
urlpatterns = [
    path("", views.forum ,name="forum" ),
    path("add/", views.addForum ,name="addFroum" ),
    path("detail/<int:id>", views.viewForum ,name="viewForum" ),
    path("detail/like/<int:id>", views.likeForum ,name="likeForum" ),
    path("detail/report/<int:id>", views.reportForum ,name="reportForum" ),
    path("detail/favYorum/<int:id>", views.likeYorum ,name="likeYorum" ),
    path("detail/deleteyorum/<int:id>", views.deleteYorum ,name="deleteYorum" ),
]