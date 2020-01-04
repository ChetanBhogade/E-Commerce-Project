from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Cart
# Create your views here.

def cart_home(request): 
    cart_id = request.session.get('cart_id', None)
    qs = Cart.objects.filter(id=cart_id)
    cart_obj = None
    
    if qs.count() == 1:
        cart_obj = qs.first()
        if request.user.is_authenticated and request.user is not None:
            cart_obj.user = request.user
            cart_obj.save()
    else:
        if request.user is not None:
            if request.user.is_authenticated:
                cart_obj = Cart.objects.create(user=request.user)
                request.session["cart_id"] = cart_obj.id
            else:
                messages.info(request, "Please Login, Before Buying Product.")
                return redirect("login")

    context = {
        'cart_obj': cart_obj
    }
    return render(request, "carts/cart-home.html", context=context)
