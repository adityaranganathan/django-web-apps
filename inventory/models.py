from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
import uuid

class CustomUserManager(BaseUserManager):
    
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError('Email field must be set')
        if extra_fields.get('is_retailer') is True and extra_fields.get('is_customer') is True:
            raise ValueError('User cannot be both Retailer and Customer')
        email = self.normalize_email(email)
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
        
    def create_user(self, email, password, **extra_fields):

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)
    
    def update_password(self, user, new_password):
        user.set_password(new_password)
        user.save()
        
class CustomUser(AbstractUser):

    username=None
    email = models.EmailField(unique=True)
    is_retailer = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
    
class RetailerManager(models.Manager):
    
    def create(self, email, password, **validated_retailer_data):
            print("Reached here ", email, password)
            user = CustomUser.objects.create_user(email, password, is_retailer=True)
            user.save()
            
            print(validated_retailer_data)
            if "gstin" in validated_retailer_data and validated_retailer_data["gstin"] == "":
                validated_retailer_data["gstin"] = None
            if "cin" in validated_retailer_data and validated_retailer_data["cin"] == "":
                validated_retailer_data["cin"] = None
            if "pan" in validated_retailer_data and validated_retailer_data["pan"] == "":
                validated_retailer_data["pan"] = None
            retailer = Retailer(user=user, **validated_retailer_data)
            retailer.save()
            return retailer
            
class Retailer(models.Model):
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,primary_key = True)
    bussiness_name = models.CharField(max_length = 500)
    address = models.CharField(max_length = 1000, null=True, blank=True)
    location = models.CharField(max_length = 1000, null=True, blank=True)
    gstin = models.CharField(max_length = 200, null=True, unique=True, blank=True)
    pan = models.CharField(max_length = 200, null=True, unique=True, blank=True)
    cin = models.CharField(max_length = 200, null=True, unique=True, blank=True)
    contactNumber = models.CharField(max_length = 200, null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    
    objects = RetailerManager()
    
    def __str__(self):
        return self.user.email
        
        
class CustomerManager(models.Manager):
    
    def create(self, email, password, **validated_customer_data):
            print("Reached here ", email, password)
            user = CustomUser.objects.create_user(email, password, is_customer=True)
            user.save()
            
            print(validated_customer_data)       
            customer = Customer(user=user, **validated_customer_data)
            customer.save()
            return customer
        
class Customer(models.Model):
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,primary_key = True)
    address = models.CharField(max_length = 1000, null=True, blank=True)
    contactNumber = models.CharField(max_length = 200, null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    
    objects = CustomerManager()
    
    def __str__(self):
        return self.user.email
            
class Merchant(models.Model):

    name = models.CharField(max_length = 200)
    contactNumber = models.CharField(max_length = 200, null=True, blank=True)
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    
    name = models.CharField(max_length = 200)
    code = models.CharField(max_length = 200, null=True, blank=True)
    stock = models.IntegerField(default = 0)
    description = models.CharField(max_length = 1000, null=True, blank=True)
    image = models.CharField(max_length = 1000, null=True, blank=True)
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name='products')
    merchant = models.ForeignKey(Merchant, on_delete=models.SET_NULL, null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['code','merchant','retailer'], name='unique_product')
        ]
    
    def __str__(self):
        return self.name