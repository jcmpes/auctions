from django.contrib import admin

# Register your models here.
from .models import Auction, Bid, Comment

admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Comment)