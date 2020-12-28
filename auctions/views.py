from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from .models import User, Listing, Bid, Comment
from .forms import ItemForm
from taggit.models import Tag
from django.template.defaultfilters import slugify
import re

def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "Listings": listings
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

def add_item(request):
    if request.method == "POST":
        listing_form = ItemForm(request.POST or None, request.FILES or None)
        if listing_form.is_valid():
            init_price = listing_form.cleaned_data['current_price']
            if int(init_price) <= 0:
                return render(request, "auctions/new_item.html", {
                    "message": "The Price must be a positive integer."
                })
            current_listing = listing_form.save(commit=False)
            current_listing.auctioneer = request.user
            current_listing.open = True
            current_listing.slug = slugify(current_listing.name)
            current_listing.save()
            listing_form.save_m2m()
            #attempt to add new item
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "auctions/new_item.html", {
            'forms': ItemForm()
        })


def listing(request, listing_id):
    current_listing = Listing.objects.get(pk=listing_id)
    listing_bid = current_listing.bidders.all()
    listing_comments = current_listing.comment.all()
    if request.user.username == current_listing.auctioneer.username:
        bid = False
    else:
        bid = True
    message = False
    if current_listing.open == False:
        if request.user.username == current_listing.current_holder:
            message = 'Congratulations, You are the Winner.'
        else:
            message = 'Sorry, This Listing has Sold.'
        if request.user.username == current_listing.auctioneer.username:
            message = f'This item has been sold on price ${current_listing.current_price}'
    return render(request, "auctions/listing.html", {
        "listing": current_listing,
        "listing_bid": listing_bid,
        'user': request.user,
        "bid": bid,
        'comments': listing_comments,
        'message': message,
    })
    
def close_bid(request, listing_id):
    current_listing = Listing.objects.get(pk=listing_id)
    current_listing.open = False
    current_listing.save()
    return listing(request, listing_id)


def new_bid(request, listing_id):
    current_listing = Listing.objects.get(pk=listing_id)
    listing_bid = current_listing.bidders.all()
    listing_comments = current_listing.comment.all()
    bid = True
    if request.method == "POST":
        bid_request = int(request.POST.get('new_bid', False))
        try:
            buyer = request.user
            r = re.compile(f'^{request.user.username}')
            if list(filter(r.match, list(map(str, listing_bid)))) != []:
                bid_new = Bid.objects.get(buyer=buyer, item=current_listing)
                if bid_request <= current_listing.current_price:
                    return render(request, 'auctions/listing.html', {
                        'listing': current_listing,
                        'listing_bid': listing_bid,
                        'bid': bid,
                        'message': 'Your bid is lower than the current price.'
                    })
                bid_new.new_bid = bid_request
            else:
                bid_new = Bid(new_bid=bid_request, buyer=request.user)
                bid_new.save()
                bid_new.item.add(current_listing)
            bid_new.save()
        except ValueError:
            return render(request, 'auctions/listing.html', {
                'listing': current_listing,
                'listing_bid': listing_bid,
                'comments': listing_comments,
                'bid': bid,
                'message1': 'Please Log In first.'
            })
        current_listing.current_price = bid_request
        current_listing.save()
        current_listing.current_holder = request.user.username
        current_listing.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'auctions/listing.html', {
                'listing': current_listing,
                'listing_bid': listing_bid,
                'comments': listing_comments,
                'bid': bid
            })

def add_watchlist(request, listing_id):
    curr_listing = Listing.objects.get(pk=listing_id)
    if request.method == 'POST':
        curr_listing.watchlisted.add(request.user)
        curr_listing.save()
        return HttpResponseRedirect(reverse('listing', args=(listing_id,)))

def remove_watchlist(request, listing_id):
    curr_listing = Listing.objects.get(pk=listing_id)
    curr_listing.watchlisted.remove(request.user)
    curr_listing.save()
    user_watchlist = request.user.watchlisted.all()
    return render(request, 'auctions/watchlist.html', {
        'listings': user_watchlist
    })

def watchlist(request):
    return render(request, 'auctions/watchlist.html', {
        'listings': request.user.watchlisted.all()
    })

def add_comment(request, listing_id):
    current_listing = Listing.objects.get(pk=listing_id)
    listing_bid = current_listing.bidders.all()
    listing_comments = current_listing.comment.all()
    if request.method == "POST":
        added_comment = request.POST.get('comment', False)
        try:
            new_comment = Comment(comment=added_comment, user=request.user)
            new_comment.save()
            new_comment.item.add(current_listing)
            new_comment.save()
        except ValueError:
            return render(request, 'auctions/listing.html', {
                'listing': current_listing,
                'listing_bid': listing_bid,
                'comments': listing_comments,
                'message1': 'Please Login First'
            })
        return HttpResponseRedirect(reverse('listing', args=(listing_id,)))
    else:
        return render(request, 'auctions/listing.html', {
                'listing': current_listing,
                'listing_bid': listing_bid,
                'comments': listing_comments,
            })

def user_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    listings = user.listings.all()
    comments = user.comments.all()
    return render(request, "auctions/profile.html", {
        'user': user,
        'listings': listings,
        'comments': comments
    })

def search_tag(request, tag):
    tag = get_object_or_404(Tag, slug=tag)
    tag_listing = Listing.objects.filter(tags=tag)
    context= {
        'tag':tag,
        'Listings': tag_listing
    }
    return render(request, 'auctions/index.html', context)

def search(request):
    input = request.POST.get('q', False)
    all_listings = list(map(str, Listing.objects.all()))
    r = re.compile(f'{input}+')
    search_listings = list(filter(r.match, all_listings))
    filtered_listings = Listing.objects.filter(name__in=search_listings)
    return render(request, 'auctions/index.html', {
        'Listings': filtered_listings
    })
