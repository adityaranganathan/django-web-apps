from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from .models import Product, Merchant, Retailer, CustomUser, Customer
from django.urls import reverse, reverse_lazy

from django.views.generic import ListView
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from .serializers import MerchantSerializer, RetailerSerializer, ProductSerializer, CustomUserSerializer, CustomerSerializer

from django.contrib.auth import authenticate, login
from django.contrib import messages

#from .forms import RetailerSignUpForm, ProductForm
from rest_framework import permissions
from .permissions import IsPostRequest, IsSuperUser, IsCorrectUser, IsProductRetailerOrReadOnly, IsCustomUserOrReadOnly#, IsRetailer,
from django.shortcuts import get_object_or_404 
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
    """
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
    return HttpResponse("Placeholder")

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
"""  
    
class CustomUserList(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsSuperUser]
       
class CustomUserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field='uuid'
    permission_classes = [IsSuperUser]
    
class RetailerList(generics.ListCreateAPIView):
    queryset = Retailer.objects.all()
    serializer_class = RetailerSerializer
    permission_classes = [IsSuperUser|IsPostRequest]

class RetailerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Retailer.objects.all()
    serializer_class = RetailerSerializer
    lookup_field='uuid'
    permission_classes = [IsSuperUser|IsCorrectUser]
    
class CustomerList(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsSuperUser|IsPostRequest]

class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_field='uuid'
    permission_classes = [IsSuperUser|IsCorrectUser]
    
class MerchantList(generics.ListCreateAPIView):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(retailer = Retailer.objects.get(user=self.request.user))
        
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Merchant.objects.all()
        retailer=Retailer.objects.get(user=self.request.user)
        return Merchant.objects.filter(retailer=retailer)

class MerchantDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer
    lookup_field='uuid'
    permission_classes = [IsSuperUser|IsCorrectUser]
    
class ProductList(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsSuperUser|IsCorrectUser]
    
    def perform_create(self, serializer):
        retailer = Retailer.objects.get(user=self.request.user)
        if self.request.data["merchantuuid"] != '':
            merchant = Merchant.objects.get(uuid = self.request.data["merchantuuid"])
            if retailer != merchant.retailer:
                raise ValueError("Merchant UUID Incorrect")
            else:
                serializer.save(retailer = retailer, merchant =  merchant)
        else:
            serializer.save(retailer = retailer, merchant =  None)
        
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Product.objects.all()
        retailer = Retailer.objects.get(user=self.request.user)
        return Product.objects.filter(retailer=retailer)
        

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field='uuid'
    permission_classes = [IsSuperUser|IsCorrectUser]
    
    def perform_update(self, serializer):
        
        retailer = Retailer.objects.get(user=self.request.user)
        if self.request.data["merchantuuid"] != '':
            merchant = Merchant.objects.get(uuid = self.request.data["merchantuuid"])
            if retailer != merchant.retailer:
                raise ValueError("Merchant UUID Incorrect")
            else:
                serializer.save(retailer = retailer, merchant =  merchant)
        else:
            serializer.save(retailer = retailer, merchant =  None)
    
    
