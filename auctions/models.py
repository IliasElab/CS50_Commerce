from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class Auction(models.Model):
    isactive = models.BooleanField(default = True)
    baseprice = models.IntegerField()
    title = models.CharField(max_length= 100)
    description = models.TextField(max_length=1500)
    image = models.URLField(max_length=200, default=None, blank=True)
    createdby = models.ForeignKey("User", on_delete=models.CASCADE , related_name="owning")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="auctions")

    def __str__(self):
        return "Auction N° "+ str(self.id)

class User(AbstractUser):
    watchlist = models.ManyToManyField(Auction, blank=True, related_name = "auctions")

class Bid(models.Model):
    value = models.IntegerField()
    proposer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="proposer_bids")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")

    class Meta:
        ordering = ('-value',)

    def __str__(self):
        return "Bid N° "+ str(self.id)

class Comment(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(max_length = 2000)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="writer_comments")
    date = models.DateTimeField(auto_now_add = True)

class Category(models.Model):
    title = models.CharField(max_length = 50)
    description = models.TextField(max_length = 500)

    def __str__(self):
        return str(self.title)
