from django.urls import path

from .views import cart_home, cart_update, checkout_home, checkout_success

app_name = 'cart'

urlpatterns = [
    path('', cart_home, name='home'),
    path('update/', cart_update, name='update'),
    path('checkout/', checkout_home, name='checkout'),
    path('success/', checkout_success, name='success'),

]
