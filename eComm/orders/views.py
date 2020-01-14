from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Order
from carts.models import Cart
# Create your views here.


def order_checkout(request):
    order_obj = None
    if request.user.is_authenticated:
        cart_obj = Cart.objects.new_or_get(request)
        if cart_obj is not None:
            if not (len(cart_obj.products.all()) == 0):
                order_obj, created = Order.objects.new_or_get(cart_obj)
            else:
                messages.warning(request, "Cart is empty now, Please add some products into cart for order.")
                return redirect("cart:home")
    else:
        messages.warning(request, "Please Login. You cannot access this page!!!")
        return redirect("login")
    context = {
        "order_obj": order_obj,
        "cart_obj": cart_obj
    }
    return render(request, "orders/checkout.html", context=context)

