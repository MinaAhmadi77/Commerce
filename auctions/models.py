from email.policy import default
from unicodedata import category
from django.contrib.auth.models import AbstractUser
from django.db import models
from matplotlib.pyplot import cla
from datetime import datetime


class User(AbstractUser):
    pass

class Categories(models.Model):
    title=models.CharField(max_length=124)

    def __str__(self):
        return f"{self.title}"
class Listings(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="userlist")
    title = models.CharField(max_length=124)
    category=models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="categories")
    discription=models.TextField()
    imgurl = models.TextField()
    starting_bid=models.FloatField()
    close= models.BooleanField(default=False)
    maxbid=models.FloatField(default=0)
    time = models.DateTimeField(default=datetime.now, blank=True)
    
    

    def __str__(self):
        return f"{self.title} ({self.starting_bid})"


class Comments(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="usercomment")
    text =models.TextField()
    listing=models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="commentlist")


    def __str__(self):
        return f"{self.id} : {self.user} to {self.listing}"


class Bids(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="userbid")
    bid=models.FloatField( default=0)
    listing=models.ForeignKey(Listings,on_delete=models.CASCADE, related_name="bidlist")

    def __str__(self):
        return f"{self.user} {self.listing} {self.bid}"

class Watch(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="userwatch")
    listing=models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="commenwatch")

    def __str__(self):
        return f"{self.id} : {self.user} to {self.listing}"
