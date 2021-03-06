from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *



def index(request):
    return render(request, "auctions/index.html", {
        "listings": Auction.objects.filter(isactive = True),
        "title": "Active Listing"
    })

def listings(request, type):
    if type == "watchlist":
        wlist = request.user.watchlist.all()
        listings = Auction.objects.filter(id__in = [wl.id for wl in wlist])
        title = "Watchlist"
    elif type == "mybids":
        blist = request.user.proposer_bids.all()
        listings = Auction.objects.filter(id__in = [bl.auction.id for bl in blist])
        title = "My Bids"
    elif type.isdigit() and int(type) in Category.objects.all().values_list('id', flat=True):
        cat = Category.objects.get(id = int(type))
        listings = Auction.objects.filter(category = cat)
        title = "Listing by " + cat.title
    else:
        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/index.html", {
        "listings": listings,
        "title": title
    })

def viewcategory(request):
    return render(request, "auctions/categorys.html", {
        "categorys": Category.objects.all()
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

@login_required
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

@login_required()
def addlisting(request):
    if request.method == "POST":
        new = Auction(
            title=request.POST["title"], 
            category = Category.objects.get(id = int(request.POST["category"])), 
            description= request.POST["description"], 
            baseprice=request.POST["baseprice"],
            image=request.POST["URL"],
            createdby=request.user)

        new.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/new_listing.html", {
            "categorys": Category.objects.all()
        })


@login_required()
def addcategory(request):
    if request.method == "POST":
        new = Category(
            title=request.POST["title"], 
            description= request.POST["description"])

        new.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/new_category.html")

 
def listing(request, listing_id):
    auction = Auction.objects.get(id = listing_id)
    watchlist = None
    message = ''

    if request.user.is_authenticated:
        watchlist = request.user.watchlist.all()

        if auction.isactive == False and auction.bids.first() and auction.bids.first().proposer == request.user:
            message = "You won this auction !"

        if request.method == "POST":
            #return HttpResponse(request.POST)
            if "Adding" in request.POST:
                request.user.watchlist.add(auction)
            elif "Removing" in request.POST:
                request.user.watchlist.remove(auction)
            elif "Bid" in request.POST and ((not auction.bids.all() and float(request.POST["Bid"]) > auction.baseprice) or (auction.bids.first() and auction.bids.first().value < float(request.POST["Bid"]))):
                new = Bid(value = float(request.POST["Bid"]), proposer = request.user, auction = auction)
                new.save()   
            elif "Closing" in request.POST:
                auction.isactive = False
                auction.save()
            elif "Commenting" in request.POST:
                comment = Comment(auction = auction, writer = request.user, content = request.POST["Commenting"])
                comment.save()
            else:
                message = "An error has been detected"

    return render(request, "auctions/listing.html", {
        "listing" : auction,
        "watchlist" : watchlist,
        "message": message
    })