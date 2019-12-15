from django.db import models

# Create your models here.	
class Seller(models.Model):
	
	name = models.CharField(max_length = 200)
	address = models.CharField(max_length = 1000)
	location = models.CharField(max_length = 1000)
	gstin = models.CharField(max_length = 200)
	pan = models.CharField(max_length = 200)
	cin = models.CharField(max_length = 200)
	contactNumber = models.CharField(max_length = 200)
	
	def __str__(self):
		return self.name
	
class Merchant(models.Model):

	name = models.CharField(max_length = 200)
	contactNumber = models.CharField(max_length = 200)
	
	def __str__(self):
		return self.name
	
class Product(models.Model):
	
	name = models.CharField(max_length = 200)
	code = models.CharField(max_length = 200)
	stock = models.IntegerField(default = 0)
	description = models.CharField(max_length = 1000)
	image = models.CharField(max_length = 1000)
	seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
	merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.name