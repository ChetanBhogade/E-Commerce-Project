from django.urls import path

from .views import order_checkout

app_name = 'order'

urlpatterns = [
    path('checkout/', order_checkout, name="checkout"),
]

