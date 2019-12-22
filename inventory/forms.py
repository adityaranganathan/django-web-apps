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
    
	name = forms.CharField(max_length = 200, required=False)
	address = forms.CharField(max_length = 1000, required=False)
	location = forms.CharField(max_length = 1000, required=False)
	gstin = forms.CharField(max_length = 50, required=False, empty_value=None)
	pan = forms.CharField(max_length = 200, required=False, empty_value=None)
	cin = forms.CharField(max_length = 200, required=False, empty_value=None)
	contactNumber = forms.CharField(max_length = 200, required=False, empty_value=None)
	
	@transaction.atomic
	def save(self):
		user = super().save(commit=False)
		user.is_retailer = True
		user.save()
        
		retailer = Retailer.objects.create(user=user)
		retailer.name = self.cleaned_data.get('name')
		retailer.address = self.cleaned_data.get('address')
		retailer.location = self.cleaned_data.get('location')
		retailer.gstin = self.cleaned_data.get('gstin')
		retailer.pan = self.cleaned_data.get('pan')
		retailer.cin = self.cleaned_data.get('cin')
		retailer.contactNumber = self.cleaned_data.get('contactNumber')
		retailer.save()
		return user
        
class ProductForm(ModelForm):
    class Meta:
        model=Product
        exclude = ['retailer']