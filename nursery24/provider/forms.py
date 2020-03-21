from django import forms
from provider.models import Address,Product,Price

class AddressForm(forms.ModelForm):
    class Meta:
        model=Address
        fields=['addr']

class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=['name','image','category']

class PriceForm(forms.ModelForm):
    class Meta:
        model=Price
        fields=['price']