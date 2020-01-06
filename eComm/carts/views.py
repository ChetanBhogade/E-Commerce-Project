from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Cart
from products.models import Product
# Create your views here.

def cart_home(request):
    cart_obj = Cart.objects.new_or_get(request=request)
    context = {
        'cart_obj': cart_obj
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
        return redirect("login")

    request.session['cart_items_count'] = cart_obj.products.all().count()
        
    return redirect("cart:home")
