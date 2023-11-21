from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:item_id>", views.showitem, name="showitem"),
    path("<int:item_id>/add", views.addbid, name="addbid"),
    path("<int:item_id>/h", views.showitem_created, name="showitem_created"),
    path("<int:item_id>/addwatch", views.addwatch, name="addwatch"),
    path("<int:item_id>/removewatch", views.removewatch, name="removewatch"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("titlecategory/<str:title>", views.titlecategory, name="titlecategory"),
    path("createlisting", views.createlisting, name="createlisting"),
    path("<int:item_id>/addcomment", views.addcomment, name="addcomment"),
    path("<int:item_id>/close", views.close, name="close")
    
    
    
]
