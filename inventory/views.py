from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from .models import Product, Merchant, Seller
from django.urls import reverse

from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from .serializers import MerchantSerializer, SellerSerializer, ProductSerializer
# Create your views here.
def index(request):
	all_products = Product.objects.all()
	template = loader.get_template('inventory/index.html')
	context = { 'all_products' : all_products}

	return HttpResponse(template.render(context, request))
	
	
def product_page(request, product_code):
	try:
		product = Product.objects.get(code = product_code)
	except Product.DoesNotExist:
		raise Http404("Product does not exist")
	template = loader.get_template('inventory/detail.html')
	context = { 'product' : product }
	print(reverse('inventory:product_page', args = [product_code]))
	return HttpResponse(template.render(context, request))
	
	
def add_product(request):
	merchant = Merchant.objects.get(id=request.POST['merchant_id'])
	seller = Seller.objects.get(id=request.POST['seller_id'])
	
	new_product = Product(name = request.POST['name'], code = request.POST['code'], description = request.POST['description'])
	new_product.image = request.POST['image']
	new_product.seller = seller
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
    

class SellerList(generics.ListCreateAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer

class SellerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    
    
class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
	
	
