from django.contrib import admin

# Register your models here.
from .models import Auction, AuctionImage, Bid, Comment


admin.site.register(Bid)
admin.site.register(Comment)

class AuctionImageAdmin(admin.StackedInline):
    model = AuctionImage

@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    inlines = [AuctionImageAdmin]

    class Meta:
        model=Auction


@admin.register(AuctionImage)
class AuctionImageAdmin(admin.ModelAdmin):
    pass


