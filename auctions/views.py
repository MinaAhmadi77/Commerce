from email import message
from pickle import TRUE
from unicodedata import category

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from .models import User,Listings,Bids,Watch,Categories,Comments
from django import forms

class NewTaskForm(forms.Form):
    task = forms.FloatField(label="Your bid $")
    # def __init__(self, min_value, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['task'].min_value = min_value

def index(request):
    # max=[]
    # for list in Listings.objects.all():
    #     maxbid=float(list.starting_bid)
    #     for i in Bids.objects.filter(listing=list):
    #         if maxbid<i.bid:
    #             maxbid=i.bid
    #     max.append(maxbid)
    return render(request, "auctions/index.html",{
      "listings": Listings.objects.all(),
    #   "max":max

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

def showitem(request,item_id):
    item=Listings.objects.get(id=item_id)
    user=request.user
    mywatch=Watch.objects.all()
    maxbid=float(item.starting_bid)
    maxuser=item.user
    comments=Comments.objects.filter(listing=item)
    closeflag=False
    bidflag=False
    bidslist=Bids.objects.filter(listing=item)
    if item.close:
        closeflag=True

    for i in Bids.objects.filter(listing=item):
        
        if maxbid<=i.bid:
            maxbid=i.bid
            maxuser=i.user    
        
    if user==item.user:
        if mywatch is None :
            bidflag=False
        else:
            for i in mywatch:
                if user==i.user and item==i.listing: 
                    bidflag=True
                else:
                    bidflag=False
        
        return render(request, "auctions/showitem_created.html",{
            "id":item_id,
            "item":item,
            "maxbid":maxbid,
            "comments":comments,
            "maxuser": maxuser,
            "bidflag":bidflag,
            "closeflag":closeflag,
            "bidslist":bidslist
            
        })  
    
        

    elif mywatch is None :         
        return render(request, "auctions/showitem.html",{
            "id":item_id,
            "item":item,
            "bidflag":False,
            "form": NewTaskForm(),
            "maxbid":maxbid,
            "comments":comments,
            "maxuser": maxuser,
            "closeflag":closeflag,
            "bidslist":bidslist
        })
    else:
        for i in mywatch:
            if user==i.user and item==i.listing:    
                return render(request, "auctions/showitem.html",{
                    "id":item_id,
                    "item":item,
                    "bidflag":True,
                    "form": NewTaskForm(),
                    "maxbid":maxbid,
                    "comments":comments,
                    "maxuser": maxuser,
                    "closeflag":closeflag,
                    "bidslist":bidslist
                }) 
        return render(request, "auctions/showitem.html",{
            "id":item_id,
            "item":item,
            "bidflag":False,
            "form": NewTaskForm(),
            "maxbid":maxbid,
            "comments":comments,
            "maxuser": maxuser,
            "closeflag":closeflag,
            "bidslist":bidslist
        })              
    
    # return render(request, "auctions/showitem.html",{
    #  "id":item_id,
    #  "item":item,
    #   "bidflag":False
     
    # })

def addbid(request,item_id):
    item=Listings.objects.get(id=item_id)
    user=User.objects.get(username=request.POST["user"])
    form = NewTaskForm(request.POST)
    mywatch=Watch.objects.all()
    maxbid=item.starting_bid
    maxuser=item.user
    comments=Comments.objects.filter(listing=item)
    bidslist=Bids.objects.filter(listing=item)
    closeflag=False
    if item.close:
        closeflag=True

  
    if form.is_valid():
        try:
            # request.POST["newbid"]
            bid= float(form.cleaned_data["task"] )
            maxbid=item.starting_bid
            start=maxbid
            n=0
            for i in Bids.objects.filter(listing=item):
                n=n+1
                
                if maxbid<=i.bid:
                    maxbid=i.bid              
                    maxuser=i.user 
            if n==0:
                if bid>=maxbid:
                    newbid = Bids.objects.create(user=user,bid=bid,listing=item)
                    newbid.save()
                    message=True   
                    maxbid=bid
                    maxuser=request.user 
                    item.maxbid=bid
                    item.save()
                else:
                    message=False

            elif bid>maxbid:
                newbid = Bids.objects.create(user=user,bid=bid,listing=item)
                newbid.save()
                message=True   
                maxbid=bid
                maxuser=request.user    
                item.maxbid=bid 
                item.save()  
                
            else:
                message=False

            if mywatch is None :         
                return render(request, "auctions/showitem.html",{
                    "id":item_id,
                    "item":item,
                    "bidflag":False,
                    "form": NewTaskForm(),
                    "maxbid":maxbid,
                    "comments":comments,
                    "message":message,
                    "maxuser": maxuser,
                    "closeflag":closeflag,
                    "bidslist":bidslist
                })
            else:
                for i in mywatch:
                    if user==i.user and item==i.listing:    
                        return render(request, "auctions/showitem.html",{
                            "id":item_id,
                            "item":item,
                            "bidflag":True,
                            "form": NewTaskForm(),
                            "maxbid":maxbid,
                            "comments":comments,
                            "message":message,
                            "maxuser": maxuser,
                            "closeflag":closeflag,
                            "bidslist":bidslist
                        }) 
                return render(request, "auctions/showitem.html",{
                    "id":item_id,
                    "item":item,
                    "bidflag":False,
                    "form": NewTaskForm(),
                    "maxbid":maxbid,
                    "comments":comments,
                    "maxuser": maxuser,
                    "message":message,
                    "closeflag":closeflag,
                    "bidslist":bidslist
                })                      
                                    

        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username kkk."
            })
    else:
        return render(request, "auctions/register.html", {
                "message": "Username already takennnnnnn."
        })
    
def showitem_created(request,item_id):
    item=Listings.objects.get(id=item_id)
    bidslist=Bids.objects.filter(listing=item)
    username=request.POST["user"]

    if username==item.user:
        return render(request, "auctions/showitem_created.html",{
            "id":item_id,
            "item":item,
            "bidflag":False,
            "bidslist":bidslist
        })  

def addwatch(request,item_id):
    item=Listings.objects.get(id=item_id)
    user=request.user
    try:
        newwatchlist =Watch.objects.create(user=user,listing=item)
        newwatchlist.save()
        return redirect('showitem', item_id )
        # return render(request, "auctions/showitem.html",{
        #     "id":item_id,
        #     "item":item,
        #     "bidflag":True
        # })  
    except IntegrityError:
        return render(request, "auctions/register.html", {
            "message": "Username already taken."
        })

def removewatch(request,item_id):
    item=Listings.objects.get(id=item_id)
    user=request.user
    try:
        mywatch=Watch.objects.get(user=user,listing=item)
        Watch.delete(mywatch)
        return redirect('showitem', item_id )
        # return render(request, "auctions/showitem.html",{
        #     "id":item_id,
        #     "item":item,
        #     "bidflag":True
        # })  
    except IntegrityError:
        return render(request, "auctions/register.html", {
            "message": "Username already taken."
        })

def watchlist(request):
    list=[]
    user=request.user
    mywatchlist=Watch.objects.filter(user=user)
    for i  in mywatchlist:
      list.append(i.listing)
    return render(request, "auctions/index.html",{
      "listings": list
    })

def categories(request):
    titles=[]
    Catego=Categories.objects.all()
    for i in Catego:
        titles.append(i.title)
     
    return render(request, "auctions/categories.html",{
      "titles": Catego,
      "flag":True
    })
def titlecategory(request,title):
    
    listing_of_category=Listings.objects.filter(category=title)
    titlenow=Categories.objects.get(id=title).title
    return render(request, "auctions/categories.html",{
      "listings": listing_of_category,
      "flag":False,
      "titlenow":titlenow
    })

def createlisting(request):
    if request.method == "POST":
        user=request.user
        title = request.POST["title"]
        category = request.POST["choose"]
        description = request.POST["description"]
        startingbid=request.POST["startingbid"]
        imageurl=request.POST["imageurl"]
        
        catego=Categories.objects.get(id=category)

        # Attempt to create new user
        try:
            listing = Listings.objects.create(user=user,title=title,category=catego,discription=description,imgurl=imageurl,starting_bid=startingbid,maxbid=startingbid)
            listing.save()
            return redirect('index')


        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
    else:
        categories=Categories.objects.all()
        return render(request, "auctions/createlisting.html",{
            "categories":categories
        })   

def addcomment(request,item_id):
    item=Listings.objects.get(id=item_id)
    user=request.user
    text=request.POST["comment"]
    try:
            comment = Comments.objects.create(user=user,text=text,listing=item,)
            comment.save()
            return redirect('showitem',item_id)


    except IntegrityError:
        return render(request, "auctions/register.html", {
            "message": "Username already taken."
        })

def close(request,item_id):
    item=Listings.objects.get(id=item_id)
    user=request.user
    mywatch=Watch.objects.all()
    maxbid=item.starting_bid
    maxuser=item.user
    comments=Comments.objects.filter(listing=item)
    bidslist=Bids.objects.filter(listing=item)
    
    for i in Bids.objects.filter(listing=item):
       
        if maxbid<=i.bid:
            maxbid=i.bid
            maxuser=i.user    
        
    item.close=True
    item.save()
    return render(request, "auctions/showitem_created.html",{
            "id":item_id,
            "item":item,
            "maxbid":maxbid,
            "comments":comments,
            "maxuser": maxuser,
            "closeflag":True,
            "bidslist":bidslist
            
    })  
    
        
