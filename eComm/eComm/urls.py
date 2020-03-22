"""eComm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include

from .views import home_page, contact_page
from products.views import search_product 
from analytics.views import (
    sales_view, 
    sales_ajax_view, 
    last_week_sales_view, 
    three_week_sales_view, 
    four_week_sales_view,
    product_analytics_view, 
    customers_analytics_view, 
    advertise_product_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path('contact/', contact_page, name='contact'),
    path('search/', search_product, name='search'),
    path('products/', include('products.urls', namespace='products')),
    path('cart/', include('carts.urls', namespace='cart')),
    path('order/', include('orders.urls', namespace='order')),
    path('account/', include('accounts.urls', namespace='account')),
    path('analytics/sales/this-week/', sales_view, name="this-week-sales-analytics"),
    path('analytics/sales/last-week/', last_week_sales_view, name="last-week-sales-analytics"),
    path('analytics/sales/three-weeks-ago/', three_week_sales_view, name="three-week-sales-analytics"),
    path('analytics/sales/four-week-ago/', four_week_sales_view, name="four-week-sales-analytics"),
    path('analytics/sales/data/', sales_ajax_view, name="sales-analytics-data"),
    path('analytics/sales/products/', product_analytics_view, name="product-analytics"),
    path('analytics/sales/customer/', customers_analytics_view, name="customer-analytics"),
    path('analytics/sales/product-advertisement/', advertise_product_view, name="product-advertisement"),

]

if settings.DEBUG :
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)