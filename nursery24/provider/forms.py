from django import forms
from provider.models import Address,Product

class AddressForm(forms.ModelForm):
    class Meta:
        model=Address
        fields=['addr']

class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=['name','image','price','category']