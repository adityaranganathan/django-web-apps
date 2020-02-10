from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import transaction

from .models import Retailer, CustomUser, Product


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)


class RetailerSignUpForm(CustomUserCreationForm):
    
    bussiness_name = forms.CharField(max_length = 200, required=False)
    address = forms.CharField(max_length = 1000, required=False)
    location = forms.CharField(max_length = 1000, required=False)
    gstin = forms.CharField(max_length = 50, required=False, empty_value=None)
    pan = forms.CharField(max_length = 200, required=False, empty_value=None)
    cin = forms.CharField(max_length = 200, required=False, empty_value=None)
    contactNumber = forms.CharField(max_length = 200, required=False, empty_value=None)
    
    @transaction.atomic
    def save(self):

        email = self.cleaned_data.pop("email")
        password = self.cleaned_data.pop("password1")
        self.cleaned_data.pop("password2")
        retailer = Retailer.objects.create(email, password, **self.cleaned_data)
        return retailer
      
        
class ProductForm(ModelForm):
    class Meta:
        model=Product
        exclude = ['retailer']
        
