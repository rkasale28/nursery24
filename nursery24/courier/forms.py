from django import forms
from courier.models import Address,Courier
from django.contrib.auth.models import User

class AddressForm(forms.ModelForm):
    class Meta:
        model=Address
        fields=['addr']

class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['email']

class CourierForm(forms.ModelForm):
    class Meta:
        model=Courier
        fields=['service_name','phone_number','profile_pic']
