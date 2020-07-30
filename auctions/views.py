from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic.detail import DetailView

# from django.views.generic import CreateView
from .forms import CreateListing, CreateListingImages

from .models import User, Auction, AuctionImage, Bid, Comment


def index(request):
    auctions = Auction.objects.filter(active=True)
    return render(request, "auctions/index.html", {"auctions": auctions})


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


# class AuctionCreateView(CreateView):
#     model = Auction
#     fields = ('title', 'starting_bid', 'description', 'image', 'category')



def create(request):
    if request.method == "POST":
        form = CreateListingImages(request.POST, request.FILES or None)
        files = request.FILES.getlist('images')
        if form.is_valid():
            
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            for f in files:
                AuctionImage.objects.create(auction=obj, image=f)
            return render(request, "auctions/index.html")

    else:
        form = CreateListingImages()
        return render(request, "auctions/create.html", {'form': form})

    
def detail(request, id):
    if request.method == "POST":
        auction = get_object_or_404(Auction, pk=id)
        if request.POST['comment']:
            comment = request.POST['comment']
            com = Comment.objects.create(user_id=request.user, auction_id=auction, comment=comment)
            return redirect('detail', id=id)
        else:   
            if request.user != auction.user:
                new_bid = request.POST['bid']
                obj = Bid.objects.create(user_id=request.user, auction_id=auction, price=new_bid)
                obj.save()
                return redirect('detail', id=id)
            else:
                auction.active = False
                auction.save()
                return redirect('detail', id=id)
    else:
        auction = get_object_or_404(Auction, pk=id)
        images = AuctionImage.objects.filter(auction=auction)
        comments = Comment.objects.all()
        context = {
            "auction": auction,
            "images": images,
            "id": id,
            "comments": comments
        }
        if auction.active == False and bid.user_id == request.user:
            context["user_won"] = request.user
        return render(request, "auctions/auction_detail.html", context)


def watchlist(request, id):
    check = Auction.objects.get(id=id)
    if check.wl.exists():
        check.wl.remove(request.user)
        check.save()
        messages.info(request, "Item was removed from your watchlist")
    else:
        check.wl.add(request.user)
        check.save()
        messages.info(request, "Item was added to your watchlist")
    return redirect('detail', id=id)


class ListingDetail(DetailView):
    model = Auction