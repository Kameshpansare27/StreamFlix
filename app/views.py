from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie,Wishlist
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.contrib import messages
import razorpay
import random

# Create your views here.


def index(req):
    return render(req, "index.html")


def validate_password(password):
    # Check minimum length
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")

    # Check maximum length
    if len(password) > 128:
        raise ValidationError("Password cannot exceed 128 characters.")

    # Initialize flags for character checks
    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False
    special_characters = "@$!%*?&"

    # Check for character variety
    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        elif char in special_characters:
            has_special = True

    if not has_upper:
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not has_lower:
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not has_digit:
        raise ValidationError("Password must contain at least one digit.")
    if not has_special:
        raise ValidationError(
            "Password must contain at least one special character (e.g., @$!%*?&)."
        )

    # Check against common passwords
    common_passwords = [
        "password",
        "123456",
        "qwerty",
        "abc123",
    ]  # Add more common passwords
    if password in common_passwords:
        raise ValidationError("This password is too common. Please choose another one.")


def signup(req):
    if req.method == "POST":
        uname = req.POST["uname"]
        email = req.POST["email"]
        upass = req.POST["upass"]
        ucpass = req.POST["ucpass"]
        context = {}
        try:
            validate_password(upass)
        except ValidationError as e:
            context["errmsg"] = str(e)
            return render(req, "signup.html", context)

        if uname == "" or email == "" or upass == "" or ucpass == "":
            context["errmsg"] = "Field can't be empty"
            return render(req, "signup.html", context)
        elif upass != ucpass:
            context["errmsg"] = "Password and confirm password doesn't match"
            return render(req, "signup.html", context)
        elif uname.isdigit():
            context["errmsg"] = "Username cannot consist solely of numbers."
            return render(req, "signup.html", context)
        else:
            try:
                userdata = User.objects.create(
                    username=uname, email=email, password=upass
                )
                userdata.set_password(upass)
                userdata.save()
                return redirect("/signin")
            except:
                context["errmsg"] = "User Already exists"
                return render(req, "signup.html", context)
    else:
        context = {}
        context["errmsg"] = ""
        return render(req, "signup.html", context)


def signin(req):
    if req.method == "POST":
        email = req.POST["email"]
        upass = req.POST["upass"]
        context = {}
        if email == "" or upass == "":
            context["errmsg"] = "Field can't be empty"
            return render(req, "signin.html", context)
        else:
            try:
                user = User.objects.get(email=email)  # Retrieve user by email
                userdata = authenticate(username=user.username, password=upass)
                print(userdata)
                if userdata is not None:
                    login(req, userdata)
                    return redirect("/membership")
                else:
                    context["errmsg"] = "Invalid username and password"
                    return render(req, "signin.html", context)
            except:
                context["errmsg"] = "User doesn't exist"
                return render(req, "signin.html", context)
    else:
        return render(req, "signin.html")


def userlogout(req):
    logout(req)
    return redirect("/")

# def membership(req):
#     return render(req,"membership.html")
def membership(req):
    if req.user.is_authenticated:
        ott = Movie.objects.filter(userid=req.user.id)
        amount = 399
        user = req.user
        client = razorpay.Client(
            auth=("rzp_test_wH0ggQnd7iT3nB", "eZseshY3oSsz2fcHZkTiSlCm")
        )
        try:
            data = {
                "amount": int(amount * 100),
                "currency": "INR",
                "receipt": str(random.randrange(1000, 90000)),
            }
            payment = client.order.create(data=data)

            context = {"data": payment, "amount": amount}
            return render(req, "membership.html", context)
        except ValidationError as e:
            context = {}
            context["errmsg"] = (
                "An error occurred while creating payment order. Please try again"
            )
            print(e)
            return render(req, "membership.html", context)
    else:
        return redirect("/mainpage")

# def membership(req):
#     if req.user.is_authenticated:
#         # Check if the user already has a membership
#         if Movie.objects.filter(userid=req.user.id).exists():
#             context = {
#                 "errmsg": "You are already a member."
#             }
#             # return render(req, "mainpage.html", context)
#             return redirect("/mainpage")

#         amount = 399
#         user = req.user
#         client = razorpay.Client(
#             auth=("rzp_test_wH0ggQnd7iT3nB", "eZseshY3oSsz2fcHZkTiSlCm")
#         )
        
#         try:
#             data = {
#                 "amount": int(amount * 100),
#                 "currency": "INR",
#                 "receipt": str(random.randrange(1000, 90000)),
#             }
#             payment = client.order.create(data=data)

#             context = {"data": payment, "amount": amount}
#             return render(req, "membership.html", context)
#         except ValidationError as e:
#             context = {
#                 "errmsg": "An error occurred while creating payment order. Please try again."
#             }
#             print(e)
#             return render(req, "membership.html", context)
#     else:
#         return redirect("/mainpage")

# def membership(req):
#     if req.user.is_authenticated:
#         # Check if the user already has a membership
#         if Movie.objects.filter(userid=req.user.id).exists():
#             context = {
#                 "errmsg": "You are already a member."
#             }
#             return render(req, "membership.html", context)

#         # Proceed with payment for new users
#         amount = 399
#         user = req.user
#         client = razorpay.Client(
#             auth=("rzp_test_wH0ggQnd7iT3nB", "eZseshY3oSsz2fcHZkTiSlCm")
#         )
        
#         try:
#             data = {
#                 "amount": int(amount * 100),  # Amount in paise
#                 "currency": "INR",
#                 "receipt": str(random.randrange(1000, 90000)),
#             }
#             payment = client.order.create(data=data)

#             context = {"data": payment, "amount": amount}
#             return render(req, "membership.html", context)
#         except ValidationError as e:
#             context = {
#                 "errmsg": "An error occurred while creating payment order. Please try again."
#             }
#             print(e)
#             return render(req, "membership.html", context)
#     else:
#         return redirect("/mainpage")


def mainpage(req):
    allmovie=Movie.objects.all()
    context={"allmovie":allmovie}
    return render(req, "mainpage.html",context)

def moviedetails(req,movieid):
    allmovie=Movie.objects.get(movieid=movieid)
    context={"allmovie":allmovie}
    return render(req, "movie-detail.html", context)

def hollywood(req):
    allmovies = Movie.moviemanager.hollywood_list
    context = {"allmovie": allmovies}
    return render(req, "mainpage.html", context)

def anime(req):
    allmovies = Movie.moviemanager.anime_list
    context = {"allmovie": allmovies}
    return render(req, "mainpage.html", context)

def video(req,movieid):
    allmovie=Movie.objects.get(movieid=movieid)
    context={"allmovie":allmovie}
    return render(req,"video.html",context)


def wishlist(req):
    user = req.user
    allwishlist = Wishlist.objects.filter(userid=user.id)

    if req.user.is_authenticated:
        context = {
            'allwishlist':allwishlist,
            'username':user,
        }
    else:
        context={
            'allwishlist':allwishlist,
        }
    return render(req, 'watchlist.html', context)


def addtofav(req,movieid):
    if req.user.is_authenticated:
        user=req.user
    else:
        user=None

    allmovie=get_object_or_404(Movie,movieid=movieid)
    wishitem,created=Wishlist.objects.get_or_create(movieid=allmovie,userid=user)
    if not created:
        wishitem.qty+=1
    else:
        wishitem.qty = 1
    wishitem.save()
    return redirect("/wishlist")

def removefavourite(req,movieid):
    user=req.user
    wishitems=Wishlist.objects.get(movieid=movieid,userid=user.id)
    wishitems.delete()
    return redirect("/wishlist")


# def wishlist(req):
#     user=req.user
#     allwishlist=Wishlist.objects.filter(userid=user.id)
#     context={"allwishlist":allwishlist}
#     return render(req,"watchlist.html",context)

# def addtofav(req,movieid):
#     if req.user.is_authenticated:
#         user=req.user
#     else:
#         user=None

#     allmovie=get_object_or_404(Movie,movieid=movieid)
#     wishitem,created=Wishlist.objects.get_or_create(movieid=allmovie,userid=user)
#     if not created:
#         wishitem.qty+=1
#     else:
#         wishitem.qty = 1
#     wishitem.save()
#     return redirect("/wishlist")

# def removefavourite(req,movieid):
#     user=req.user
#     wishitems=Wishlist.objects.get(movieid=movieid,userid=user.id)
#     wishitems.delete()
#     return redirect("/mainpage")