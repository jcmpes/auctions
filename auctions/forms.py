from django import forms
from django.http import request

from .models import Auction

class CreateListing(forms.ModelForm):

    class Meta:
        model = Auction
        fields = ['title', 'description', 'starting_bid', 'image', 'category']