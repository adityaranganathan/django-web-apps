from django.contrib import admin

from.models import Product, Merchant, Seller
# Register your models here.
admin.site.register(Product)
admin.site.register(Merchant)
admin.site.register(Seller)