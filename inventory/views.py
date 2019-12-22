from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from .models import Product, Merchant, Retailer, CustomUser
from django.urls import reverse, reverse_lazy

from django.views.generic import ListView
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from .serializers import MerchantSerializer, RetailerSerializer, ProductSerializer

from django.contrib.auth import authenticate, login
from django.contrib import messages

from .forms import RetailerSignUpForm, ProductForm

# Create your views here.
def index(request):
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pwd']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Succesfully logged in as {}!'.format(email))
            return HttpResponseRedirect(reverse('inventory:products_list'))
        else:
            messages.add_message(request, messages.INFO, 'Incorrect credentials')
    
    return render(request, 'inventory/index.html')
    
def sign_up_retailer(request):
    if request.method == 'POST':
        sign_up_form = RetailerSignUpForm(request.POST)
        if sign_up_form.is_valid():
            sign_up_form.save()
            name = sign_up_form.cleaned_data.get('name')
            messages.add_message(request, messages.SUCCESS, 'Succesfully created {}!'.format(name))
            return HttpResponseRedirect(reverse_lazy('inventory:home'))
        else:
            messages.add_message(request, messages.INFO, 'Invalid Form!')
            return HttpResponseRedirect(reverse_lazy('inventory:sign_up_retailer'))
    else:
        sign_up_form = RetailerSignUpForm()
    return render(request, 'inventory/signup.html', context={'form':sign_up_form})
    
def sign_up_customer(request):
    if request.method == 'POST':
        sign_up_form = UserCreationForm(request.POST)
        if sign_up_form.is_valid():
            sign_up_form.save()
            username = sign_up_form.cleaned_data.get('username')
            messages.add_message(request, messages.SUCCESS, 'Succesfully created {}!'.format(username))
            return HttpResponseRedirect(reverse_lazy('inventory:home'))
        else:
            messages.add_message(request, messages.INFO, 'Invalid Form!')
            return HttpResponseRedirect(reverse_lazy('inventory:sign_up'))
    else:
        sign_up_form = UserCreationForm()
    return render(request, 'inventory/signup.html', context={'form':sign_up_form})
    


def products_list(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy('inventory:home'))
    else:
        if request.method == 'POST':
            add_productform = ProductForm(request.POST)
            new_product = add_productform.save(commit=False)
            new_product.retailer = Retailer.objects.get(user=request.user)
            new_product.save()
            messages.add_message(request, messages.SUCCESS, 'Succesfully Added {}!'.format(request.POST['name']))
        else:
            add_productform = ProductForm(request.POST)
        products = Product.objects.filter(retailer = Retailer.objects.get(user=request.user))
    return render(request, 'inventory/products.html', context={'products':products, 'form':add_productform})
    
    
def add_product(request):
    merchant = Merchant.objects.get(id=request.POST['merchant_id'])
    retailer = Retailer.objects.get(id=request.POST['retailer_id'])
    
    new_product = Product(name = request.POST['name'], code = request.POST['code'], description = request.POST['description'])
    new_product.image = request.POST['image']
    new_product.retailer = retailer
    new_product.merchant = merchant
    new_product.save()
    s = ""
    for key, value in request.POST.items():
        s += str(key) + ":" + str(value) + "|||"
    return HttpResponseRedirect('/inventory')
    
def watever(request, x, y):
    return HttpResponse(str(x)+str(y))
    
class MerchantList(generics.ListCreateAPIView):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer

class MerchantDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer
    

class RetailerList(generics.ListCreateAPIView):
    queryset = Retailer.objects.all()
    serializer_class = RetailerSerializer

class RetailerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Retailer.objects.all()
    serializer_class = RetailerSerializer
    
    
class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    
