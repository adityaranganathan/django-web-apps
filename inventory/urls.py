from django.urls import path, include
from . import views


api_patterns = [
	path('merchants/', views.MerchantList.as_view()),
    path('merchants/<int:pk>/', views.MerchantDetail.as_view()),
    path('sellers/', views.SellerList.as_view()),
    path('sellers/<int:pk>/', views.SellerDetail.as_view()),
    path('products/', views.ProductList.as_view()),
    path('products/<int:pk>/', views.ProductDetail.as_view()),
    
]

app_name = 'inventory'
urlpatterns = [
	path('', views.index, name='index'),
	path('<int:product_code>/', views.product_page, name='product_page'),
	path('add_product/', views.add_product, name='add_product'),
	path('watever/<x>/<y>/', views.watever, name='watever_page'),
	path('api/', include(api_patterns)),
]

