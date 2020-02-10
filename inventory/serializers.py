from rest_framework import serializers
from .models import Product, Merchant, Retailer, CustomUser, Customer

class ProductSerializer(serializers.ModelSerializer):

    retailer = serializers.ReadOnlyField(source='retailer.user.email')
    url = serializers.HyperlinkedIdentityField(view_name="inventory:product-detail", lookup_field='uuid')
    merchantuuid = serializers.CharField(max_length=100, write_only=True, required=False, allow_null=True)
    merchant_name = serializers.ReadOnlyField(source='merchant.name')
    
    class Meta:
        model = Product
        fields = ('name', 'code', 'stock', 'description', 'image',  'merchantuuid','retailer', 'merchant_name', 'url')
        
    def create(self, validated_data):
        validated_data.pop("merchantuuid")
        return Product.objects.create(**validated_data)
        
class MerchantSerializer(serializers.ModelSerializer):

    retailer = serializers.ReadOnlyField(source='retailer.user.email')
    url = serializers.HyperlinkedIdentityField(view_name="inventory:merchant-detail", lookup_field='uuid')
    
    class Meta:
        model = Merchant
        fields = ('name', 'contactNumber', 'retailer', 'uuid', 'url')
        
class CustomUserSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name="inventory:customuser-detail", lookup_field='uuid')
    
    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'url')
        extra_kwargs = {'password': {'write_only': True}}

        
class RetailerSerializer(serializers.HyperlinkedModelSerializer):

    user = CustomUserSerializer()
    url = serializers.HyperlinkedIdentityField(view_name="inventory:retailer-detail", lookup_field='uuid')
    products = serializers.PrimaryKeyRelatedField(many=True, required=False, queryset=Product.objects.all())
    
    class Meta:
        model = Retailer
        fields = ('user', 'bussiness_name', 'address', 'location', 'gstin', 'pan', 'cin', 'contactNumber', 'url', 'products')
        
    def create(self, validated_data):

        if "products" in validated_data:
            validated_data.pop("products")
        user = validated_data.pop('user')
        return Retailer.objects.create(user["email"], user["password"], **validated_data)
        
    def update(self, instance, validated_data):
        
        if "user" in validated_data:
            if "email" in validated_data["user"]:
                raise ValueError("Email cannot be updated")
            if "password" in validated_data["user"]:
                CustomUser.objects.update_password(instance.user, validated_data["user"]["password"])
        instance.bussiness_name = validated_data.get("bussiness_name", instance.bussiness_name)
        instance.address = validated_data.get("address", instance.address)
        instance.location = validated_data.get("location", instance.location)
        instance.gstin = validated_data.get("gstin", instance.gstin)
        instance.pan = validated_data.get("pan", instance.pan)
        instance.cin = validated_data.get("cin", instance.cin)
        instance.contactNumber = validated_data.get("contactNumber", instance.contactNumber)
        instance.save()
        return instance
        
class CustomerSerializer(serializers.HyperlinkedModelSerializer):

    user = CustomUserSerializer()
    url = serializers.HyperlinkedIdentityField(view_name="inventory:customer-detail", lookup_field='uuid')
    
    class Meta:
        model = Customer
        fields = ('user', 'address', 'contactNumber', 'url')
        
    def create(self, validated_data):
        user = validated_data.pop('user')
        return Customer.objects.create(user["email"], user["password"], **validated_data)
        
    def update(self, instance, validated_data):
        
        if "user" in validated_data:
            if "email" in validated_data["user"]:
                raise ValueError("Email cannot be updated")
            if "password" in validated_data["user"]:
                CustomUser.objects.update_password(instance.user, validated_data["user"]["password"])
        instance.address = validated_data.get("address", instance.address)
        instance.contactNumber = validated_data.get("contactNumber", instance.contactNumber)
        instance.save()
        return instance
        