from django.contrib import admin

from.models import CustomUser, Product, Merchant, Retailer, Customer
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm#, RetailerCreationForm, RetailerChangeForm

admin.site.register(Product)
admin.site.register(Merchant)
admin.site.register(Customer)
admin.site.register(Retailer)

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['email', 'is_retailer', 'is_customer', 'is_staff', 'is_active','is_superuser', 'date_joined']
    
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    readonly_fields = ['date_joined',]

admin.site.register(CustomUser, CustomUserAdmin)