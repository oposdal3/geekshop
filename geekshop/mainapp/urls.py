from django.urls import path
from mainapp.views import products

app_name = 'mainapp'

urlpatterns = [
    path('', products, name='index'),
    path('product/<int:pk>/', products, name='products'),
    path('products_all/', products, name='products_all'),
    path('products_home/', products, name='products_home'),
    path('products_office/', products, name='products_office'),
    path('products_modern/', products, name='products_modern'),
    path('products_classic/', products, name='products_classic'),

]
