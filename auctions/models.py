from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    def image():
        return 'https://www.thebluediamondgallery.com/wooden-tile/images/auction.jpg'

    user = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.IntegerField()
    category = models.CharField(max_length=64)
    link = models.CharField(max_length=350, default=image())
    time = models.DateTimeField()
    closed = models.BooleanField(default=False)
    watch = models.ManyToManyField(User, blank=True, related_name='watch')


    def __str__(self):
        return self.title

class Bid(models.Model):
    user = models.CharField(max_length=64)
    bid = models.IntegerField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')

    def __str__(self):
        return f'{self.bid}'

class Comment(models.Model):
    user = models.CharField(max_length=64)
    time = models.DateTimeField()
    content = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'{self.content}'
