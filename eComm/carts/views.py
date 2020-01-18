from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Cart
from products.models import Product
from accounts.forms import AddressForm
from accounts.models import BillingProfile
# Create your views here.

def cart_home(request):
    cart_obj = Cart.objects.new_or_get(request=request)
    is_empty = True
    if cart_obj is not None:
        length = len(cart_obj.products.all())
        if length == 0:
            is_empty = True
        else:
            is_empty = False

    context = {
        'cart_obj': cart_obj,
        "is_empty": is_empty
    }
    return render(request, "carts/cart-home.html", context=context)


def cart_update(request):
    if request.user.is_authenticated:
        product_id = request.POST.get('product_id')
        if product_id is not None:
            try:
                product_obj = Product.objects.get_by_id(id=product_id)
            except:
                messages.error(request, "Error Occur!!! Product is gone.")
        else:
            return redirect("product:product-list")

        cart_obj = Cart.objects.new_or_get(request=request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
        else:
            cart_obj.products.add(product_obj)
    else:
        messages.warning(request, "Please Login, before buying a product.")
        return redirect("login")

    request.session['cart_items_count'] = cart_obj.products.all().count()
        
    return redirect("cart:home")


def checkout_home(request):
    order_obj = None
    if request.user.is_authenticated:
        cart_obj = Cart.objects.new_or_get(request)
        if cart_obj.products.count() == 0:
            messages.info(request, "Cart is empty now!")
            return redirect("cart:home")
        address_form = AddressForm(request.POST)

        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request=request)





    else:
        messages.warning(request, "Please login, you cannot access this page.")
        return redirect("login")


    context = {
        'address_form': address_form,
        'cart_obj': cart_obj,
        'order_obj': order_obj,
        'billing_profile': billing_profile
    }
    return render(request, "carts/checkout.html", context=context)























# def order_checkout(request):
#     order_obj = None
#     if request.user.is_authenticated:
#         cart_obj = Cart.objects.new_or_get(request)
#         if cart_obj is not None:
#             if not (len(cart_obj.products.all()) == 0):
#                 order_obj, created = Order.objects.new_or_get(cart_obj)
#                 address_form = AddressForm()
                




#             else:
#                 messages.warning(request, "Cart is empty now, Please add some products into cart for order.")
#                 return redirect("cart:home")
#     else:
#         messages.warning(request, "Please Login. You cannot access this page!!!")
#         return redirect("login")
#     context = {
#         "order_obj": order_obj,
#         "cart_obj": cart_obj,
#         "form": address_form
#     }
#     return render(request, "orders/checkout.html", context=context)

