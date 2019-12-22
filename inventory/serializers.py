from rest_framework import serializers
from .models import Product, Merchant, Retailer

class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ('id', 'name', 'code', 'stock', 'description', 'image', 'retailer', 'merchant')
        
class MerchantSerializer(serializers.ModelSerializer):
	class Meta:
		model = Merchant
		fields = ('id', 'name', 'contactNumber')
        
class RetailerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Retailer
		fields = ('id', 'name', 'address', 'location', 'gstin', 'pan', 'cin', 'contactNumber')