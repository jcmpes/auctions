from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass


def user_directory_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Auction(models.Model):
    CATEGORIES = [
        ('TO', 'Toys'),
        ('EL', 'Electronics'),
        ('HO', "Home"),
        ('FA', "Fashion"),
        ('OT', "Other")
        
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2)
    title = models.CharField(max_length=60)
    description = models.TextField(blank=False)
    image = models.ImageField(upload_to=user_directory_path)
    category = models.CharField(max_length=2, choices=CATEGORIES)

    def __str__(self):
        return '{} | {}'.format(self.user, self.title)

class Bid(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    auction_id = models.ForeignKey(Auction, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)


class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=60)
    comment = models.TextField(blank=False)