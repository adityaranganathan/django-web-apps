from rest_framework import serializers
from .models import Product, Merchant, Seller

class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ('id', 'name', 'code', 'stock', 'description', 'image', 'seller', 'merchant')
        
class MerchantSerializer(serializers.ModelSerializer):
	class Meta:
		model = Merchant
		fields = ('id', 'name', 'contactNumber')
        
class SellerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Seller
		fields = ('id', 'name', 'address', 'location', 'gstin', 'pan', 'cin', 'contactNumber')