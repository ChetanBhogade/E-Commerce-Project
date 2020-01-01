from django.urls import path

from .views import product_list, product_detail 

app_name = 'products'

urlpatterns = [
    path('', product_list, name='product-list'),
    path('<str:slug>/', product_detail, name='product-detail'),

]
