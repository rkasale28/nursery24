from django import forms
from deliveryPersonnel.models import DeliveryPersonnel
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','first_name','last_name','email']

class DeliveryPersonnelForm(forms.ModelForm):
    class Meta:
        model=DeliveryPersonnel 
        fields=['phone_number','profile_pic']

class UpdateForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','email']
