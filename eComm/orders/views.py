from django.shortcuts import render

from .models import Order
from carts.models import Cart
from accounts.models import BillingProfile
# Create your views here.

def order_history_page(request):
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    order_obj = Order.objects.filter(billing_profile=billing_profile)
    context = {
        'order_obj': order_obj,
    }
    return render(request, "orders/order-history-list.html", context=context)


