from django.urls import path

from .views import cart_home, cart_update, checkout_home, checkout_success, payment_page_view

app_name = 'cart'

urlpatterns = [
    path('', cart_home, name='home'),
    path('update/', cart_update, name='update'),
    path('checkout/', checkout_home, name='checkout'),
    path('success/', checkout_success, name='success'),
    path('payment/online/', payment_page_view, name='payment_page'),

]
