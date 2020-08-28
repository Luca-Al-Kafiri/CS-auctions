from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Comment


def index(request):
    items = Listing.objects.all()
    return render(request, "auctions/index.html", {'items': items})

def listing(request, id):
    item = Listing.objects.get(id=id)
    comment = item.comments.all()
    bids= item.bids.all().order_by('-bid')
    winner = item.bids.last()
    if request.method == 'POST':
        item.closed = True
        item.save()
        return render(request, 'auctions/listing.html', {"i":item, 'c':comment, 'winner':winner})
    else:    
        return render(request, 'auctions/listing.html', {"i":item, 'c':comment, 'winner':winner})

@login_required
def create(request):
    if request.method == 'POST':
        new_listing = Listing()
        new_listing.user = request.user.username
        new_listing.title = request.POST.get('title')
        new_listing.description = request.POST.get('description')
        new_listing.price = request.POST.get('price')
        new_listing.category = request.POST.get('category')
        new_listing.link = request.POST.get('link')
        new_listing.time = datetime.datetime.now()
        new_listing.save()
        return redirect('listing', id=new_listing.id)
    else:
        return render(request, 'auctions/create.html')

@login_required
def bid(request, id):
    if request.method == "POST":
        price = int(request.POST.get('bid'))
        item = Listing.objects.get(id=id)
        comment = item.comments.all()
        bids= item.bids.all().order_by('-bid')
        current_price = item.price
        if price > current_price:
            item.price = price
            item.save()
            b = Bid()
            b.user = request.user.username
            b.bid = price
            b.listing = Listing.objects.get(id=id)
            b.save()
            return redirect('listing', id=id)
        else:
            return render(request,'auctions/listing.html', {'i': item,'c':comment, 'b':bids, 'message':'Your bid is not higher than the current price'})

@login_required
def comment(request, id):
    if request.method == 'POST':
        comment = Comment()
        comment.user = request.user.username
        comment.time = datetime.datetime.now()
        comment.content = request.POST.get('content')
        comment.listing = Listing.objects.get(id=id)
        comment.save()
        return redirect('listing', id=id)

@login_required
def watch(request, id):
    if request.method == 'POST':
        item = Listing.objects.get(id=id)
        user = User.objects.get(id=request.user.id)
        item.watch.add(user)
        comment = item.comments.all()
        bids= item.bids.all().order_by('-bid')
        return render(request,'auctions/listing.html', {'i': item,'c':comment, 'b':bids, 'message':'Added to watch list'})

@login_required
def watchlist(request):
    user = User.objects.get(id=request.user.id)
    items = user.watch.all()
    return render(request, 'auctions/watchlist.html', {'items':items})

@login_required
def remove(request, id):
    user = User.objects.get(id=request.user.id)
    item = Listing.objects.get(id=id)
    user.watch.remove(item)
    return redirect('watchlist')

@login_required
def cats(request):
    items = Listing.objects.values('category').distinct()
    return render(request, 'auctions/cats.html', {'items':items})

@login_required
def cat(request, category):
    items = Listing.objects.filter(category=category)
    return render(request, 'auctions/cat.html', {'items':items})

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
