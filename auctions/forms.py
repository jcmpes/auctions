from django import forms
from django.http import request

from .models import Auction

class CreateListing(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'description', 'starting_bid', 'category', 'image']

class CreateListingImages(CreateListing):
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta(CreateListing.Meta):
        fields = CreateListing.Meta.fields + ['images',]