from django.views.generic import ListView, DetailView
from django.shortcuts import render, Http404
from django.contrib import messages

from .models import Product
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
    except:
        raise Http404("Product Doesn't Exists.")
    context = {
        "product": instance
    }
    return render(request, "products/product_detail.html", context=context)
    

def search_product(request):
    query = request.GET.get('query', None)
    if query is not None:
        qs1 = Product.objects.filter(title__icontains = query)
        qs2 = Product.objects.filter(description__icontains = query)
        result = qs1.union(qs2)
    else:
        result = Product.objects.none()

    if len(query) < 1:
        messages.warning(request, "Please enter some query for search.")
    context = {
        "result": result,
        "query": query
    }
    return render(request, "search/view.html", context=context)

