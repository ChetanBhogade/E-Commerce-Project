from django.urls import path

from .views import account_home_page, login_page, logout_page, register_page, address_create_view

app_name = 'account'

urlpatterns = [
    path('home/', account_home_page, name='account-home'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('register/', register_page, name='register'),
    path('address/create/view/', address_create_view, name='address_create_view'),
]