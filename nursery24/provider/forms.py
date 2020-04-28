from django import forms
from provider.models import Address,Product,Price,Provider
from django.contrib.auth.models import User

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

class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','email']

class ProviderForm(forms.ModelForm):
    class Meta:
        model=Provider
        fields=['shop_name','phone_number','profile_pic']
