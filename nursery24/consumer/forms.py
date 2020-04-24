from django import forms
from provider.models import Address,Product,Price

class AddressForm(forms.ModelForm):
    class Meta:
        model=Address
        fields=['addr']