from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .managers import CustomUserManager
from django.conf import settings
from django.utils import timezone

class CustomUser(AbstractUser):

    username=None
    email = models.EmailField(unique=True)
    is_retailer = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
    
class Retailer(models.Model):
	
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
	name = models.CharField(max_length = 200)
	address = models.CharField(max_length = 1000, null=True, blank=True)
	location = models.CharField(max_length = 1000, null=True, blank=True)
	gstin = models.CharField(max_length = 200, null=True, unique=True, blank=True)
	pan = models.CharField(max_length = 200, null=True, unique=True, blank=True)
	cin = models.CharField(max_length = 200, null=True, unique=True, blank=True)
	contactNumber = models.CharField(max_length = 200, null=True, blank=True)
	
	def __str__(self):
		return self.user.email
	
class Merchant(models.Model):

	name = models.CharField(max_length = 200)
	contactNumber = models.CharField(max_length = 200, null=True, blank=True)
	retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.name
	
class Product(models.Model):
	
	name = models.CharField(max_length = 200)
	code = models.CharField(max_length = 200, null=True, blank=True)
	stock = models.IntegerField(default = 0)
	description = models.CharField(max_length = 1000, null=True, blank=True)
	image = models.CharField(max_length = 1000, null=True, blank=True)
	retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE)
	merchant = models.ForeignKey(Merchant, on_delete=models.SET_NULL, null=True, blank=True)
	
	class Meta:
		constraints = [
			models.UniqueConstraint(fields=['code','merchant','retailer'], name='unique_product')
		]
	
	def __str__(self):
		return self.name