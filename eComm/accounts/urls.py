from django.urls import path

from .views import account_home_page, login_page, logout_page, register_page, address_create_view, update_profile
from orders.views import order_history_page
from analytics.views import user_product_history

app_name = 'account'

urlpatterns = [
    path('home/', account_home_page, name='account-home'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('register/', register_page, name='register'),
    path('address/create/view/', address_create_view, name='address_create_view'),
    path('order/history', order_history_page, name='order_history'),
    path('user/history', user_product_history, name='user_history'),
    path('user/profile/update/', update_profile, name='update_profile'),
]