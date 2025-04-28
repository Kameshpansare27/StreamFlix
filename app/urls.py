from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("mainpage/", views.mainpage, name="mainpage"),
    path("membership/", views.membership, name="membership"),
    path('moviedetails/<int:movieid>/', views.moviedetails, name="moviedetails"),
    path("userlogout/", views.userlogout, name="userlogout"),
    path("hollywood/", views.hollywood, name="hollywood"),
    path("anime/", views.anime, name="anime"),
    path("video/<int:movieid>",views.video,name="video"),
    path("wishlist/",views.wishlist,name="wishlist"),
    path("removefavourite/<int:movieid>",views.removefavourite,name="removefavourite"),
    path("addtofav/<int:movieid>",views.addtofav,name="addtofav"),
     
]