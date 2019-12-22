from django.urls import path, include
from . import views


api_patterns = [
	path('merchants/', views.MerchantList.as_view()),
    path('merchants/<int:pk>/', views.MerchantDetail.as_view()),
    path('retailers/', views.RetailerList.as_view()),
    path('retailers/<int:pk>/', views.RetailerDetail.as_view()),
    path('products/', views.ProductList.as_view()),
    path('products/<int:pk>/', views.ProductDetail.as_view()),   
]

app_name = 'inventory'
urlpatterns = [
	path('', views.index, name='home'),
	path('signup/retailer/', views.sign_up_retailer, name='sign_up_retailer'),
	path('signup/customer/', views.sign_up_customer, name='sign_up_customer'),
	path('products/', views.products_list, name='products_list'),
	path('api/', include(api_patterns)),
]

