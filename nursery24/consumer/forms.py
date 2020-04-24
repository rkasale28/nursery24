from django import forms
from consumer.models import Address,Consumer
from django.contrib.auth.models import User

class AddressForm(forms.ModelForm):
    class Meta:
        model=Address
        fields=['addr']

class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','email']

class ConsumerForm(forms.ModelForm):
    class Meta:
        model=Consumer
        fields=['phone_number']
