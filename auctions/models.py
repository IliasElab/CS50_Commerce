from django.contrib.auth.models import AbstractUser
from django.db import models



class Auction(models.Model):
    isactive = models.BooleanField(default = True)
    price = models.ForeignKey("Bid", on_delete=models.CASCADE, related_name="bid_auction", null=True)
    title = models.CharField(max_length= 100)
    description = models.TextField(max_length=1500)
    category = models.CharField(max_length= 50, default=None)
    image = models.URLField(max_length=200, default=None, blank=True)
    createdby = models.ForeignKey("User", on_delete=models.CASCADE , related_name="owning")

class User(AbstractUser):
    watchlist = models.ManyToManyField(Auction, blank=True, related_name = "auctions")

class Bid(models.Model):
    value = models.IntegerField()
    proposer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="proposer_bids")

    def __str__(self):
        return "Bid N° "+ str(self.id)

class Comment(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")


# old models
# class Auction(models.Model):
#     isactive = models.BooleanField(default = True)
#     baseprice = models.FloatField(max_length=20)
#     price = models.FloatField(max_length=20)
#     title = models.CharField(max_length= 100)
#     description = models.TextField(max_length=1500)
#     category = models.CharField(max_length= 50, default=None)
#     image = models.URLField(max_length=200, default=None, blank=True)
#     createdby = models.ForeignKey("User", on_delete=models.CASCADE , related_name="owning")

# class User(AbstractUser):
#     watchlist = models.ManyToManyField(Auction, blank=True, related_name = "auctions")

# class Bid(models.Model):
#     auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="auction_bids")
#     value = models.IntegerField()
#     proposer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="proposer_bids")

# class Comment(models.Model):
#     auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")
