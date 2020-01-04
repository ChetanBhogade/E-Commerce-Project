from django.urls import path

from .views import cart_home

app_name = 'products'

urlpatterns = [
    path('', cart_home, name='home'),
    # path('<str:slug>/', product_detail, name='product-detail'),

]
