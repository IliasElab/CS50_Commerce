from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Auction.objects.filter(isactive = True)
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def addlisting(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            new = Auction(
                title=request.POST["title"], 
                category = request.POST["category"], 
                description= request.POST["description"], 
                price=request.POST["baseprice"], 
                image=request.POST["URL"],
                createdby=request.user)


            new.save()
            return render(request, "auctions/index.html", {
                "listings": Auction.objects.filter(isactive = True)
            })
        else:
            return render(request, "auctions/new_listing.html")
    else:
        return render(request, "auctions/login.html")

 
def listing(request, listing_id):
    auction = Auction.objects.get(id = listing_id)
    watchlist = None

    if request.method == "POST" and request.user.is_authenticated:
        if "Adding" in request.POST:
            request.user.watchlist.add(auction)
        elif "Removing" in request.POST:
            request.user.watchlist.remove(auction)
        else:
            return HttpResponse("Done erroring")

    if request.user.is_authenticated:
        watchlist = request.user.watchlist.all()

    return render(request, "auctions/listing.html", {
        "listing" : auction,
        "watchlist" : watchlist
    })