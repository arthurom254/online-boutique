from django import forms
from .models import Item, Category, DeliveryLocation, Locations
class AddItems(forms.ModelForm):
    class Meta:
        model=Item
        fields="__all__"

class AddCategory(forms.ModelForm):
    class Meta:
        model=Category
        fields="__all__"

class DeliveryLocationForm(forms.ModelForm):
    class Meta:
        model=DeliveryLocation
        fields="__all__"

class LocationsForm(forms.ModelForm):
    class Meta:
        model=Locations
        fields="__all__"