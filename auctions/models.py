from django.contrib.auth.models import AbstractUser
from django.db import models
from taggit.managers import TaggableManager
from django.template.defaultfilters import slugify
class User(AbstractUser):
    pass

class Listing(models.Model):
    name = models.CharField(max_length=64, blank=False)
    desc = models.TextField(max_length=255, blank=False)
    auctioneer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    open = models.BooleanField(default=True)
    current_price = models.IntegerField(default=0, blank=False)
    current_holder = models.CharField(max_length=64, default='')
    watchlisted = models.ManyToManyField(User, blank=True, default=None, related_name="watchlisted")
    image = models.ImageField(upload_to='media/images/', default='images/no-image.png')

    slug = models.SlugField(max_length=100, default=slugify(name))
    tags = TaggableManager(related_name='tags')

    def __str__(self):
        return f'{self.name}'


class Bid(models.Model):
    new_bid = models.IntegerField()
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="biddings")
    item = models.ManyToManyField(Listing, blank=True, related_name="bidders")

    def __str__(self):
        return f'{self.buyer.username}: ${self.new_bid}'
    
class Comment(models.Model):
    item = models.ManyToManyField(Listing, blank=True, related_name='comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', default=None)
    comment = models.TextField(max_length=255)
