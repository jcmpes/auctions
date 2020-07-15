from django import forms

from .models import Auction

class CreateListing(forms.ModelForm):

    class Meta:
        model = Auction
        fields = ['user', 'title', 'description', 'starting_bid', 'category']