from django.urls import path

from .views import account_home_page, login_page, logout_page, register_page, address_create_view
from orders.views import order_history_page

app_name = 'account'

urlpatterns = [
    path('home/', account_home_page, name='account-home'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('register/', register_page, name='register'),
    path('address/create/view/', address_create_view, name='address_create_view'),
    path('order/history', order_history_page, name='order_history'),
]