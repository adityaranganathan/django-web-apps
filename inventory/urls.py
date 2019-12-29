from django.urls import path, include
from . import views

api_patterns = [
    path('merchants/', views.MerchantList.as_view()),
    path('merchants/<str:uuid>/', views.MerchantDetail.as_view(), name = "merchant-detail"),
    path('users/', views.CustomUserList.as_view()),
    path('users/<str:uuid>/', views.CustomUserDetail.as_view(), name="customuser-detail"),
    path('retailers/', views.RetailerList.as_view()),
    path('retailers/<str:uuid>/', views.RetailerDetail.as_view(), name="retailer-detail"),
    path('customers/', views.CustomerList.as_view()),
    path('customers/<str:uuid>/', views.CustomerDetail.as_view(), name="customer-detail"),
    path('products/', views.ProductList.as_view()),
    path('products/<str:uuid>/', views.ProductDetail.as_view(), name="product-detail"),    
]

#from rest_framework import routers

#router = routers.DefaultRouter()
#router.register(r'retailers', views.RetailerViewSet)


urlpatterns = [
    #path('', views.index, name='home'),
    #path('apir/', include(router.urls)),
    #path('signup/retailer/', views.sign_up_retailer, name='sign_up_retailer'),
    #path('signup/customer/', views.sign_up_customer, name='sign_up_customer'),
    #path('products/', views.products_list, name='products_list'),
    path('api/', include(api_patterns)),
]

