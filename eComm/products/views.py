from django.shortcuts import render, Http404
from django.contrib import messages

from .models import Product
from carts.models import Cart
from analytics.signals import object_viewed_signal
from analytics.views import product_total_views
# Create your views here.

def product_list(request):
    queryset = Product.objects.all()
    context = {
        "all_products": queryset
    }
    return render(request, "products/product_list.html", context=context)


def product_detail(request, *args, **kwargs):
    slug = kwargs.get('slug')
    try:
        instance = Product.objects.get(slug=slug)
        cart_obj = Cart.objects.new_or_get(request=request)
    except:
        raise Http404("Product Doesn't Exists.")
    context = {
        "product": instance,
        "cart": cart_obj,
        "prod_views_dict": product_total_views()
    }

    object_viewed_signal.send(instance.__class__, instance=instance, request=request)
    return render(request, "products/product_detail.html", context=context)
    

def search_product(request):
    query = request.GET.get('query', None)
    if query is not None:
        qs1 = Product.objects.filter(title__icontains = query)
        qs3 = Product.objects.filter(category__icontains = query)
        qs2 = Product.objects.filter(description__icontains = query)
        result = qs1.union(qs2, qs3)
    else:
        result = Product.objects.none()

    if len(query) < 1:
        messages.warning(request, "Please enter some query for search.")
    context = {
        "result": result,
        "query": query
    }
    return render(request, "search/view.html", context=context)

