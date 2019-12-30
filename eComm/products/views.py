from django.views.generic import ListView, DetailView
from django.shortcuts import render, Http404
from django.contrib import messages

from .models import Product
# Create your views here.

class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = 'products/product_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        # context = {'paginator': None, 'page_obj': None, 'is_paginated': False, 'object_list': <QuerySet [<Product: Hat>]>, 'product_list': <QuerySet [<Product: Hat>]>, 'view': <products.views.ProductListView object at 0x000001C906301390>}
        return context


class ProductDetailView(DetailView):
    # queryset = Product.objects.all()
    template_name = 'products/product_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        # context = {'object': <Product: Hat>, 'product': <Product: Hat>, 'view': <products.views.ProductDetailView object at 0x0000019202F6B630>}
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        try:
            instance = Product.objects.get(slug=slug)
        except :
            raise Http404("Product Doesn't Exists.")
        return instance

    

class SearchProductView(ListView):
    template_name = 'search/view.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        query = request.GET.get('q', None)
        if query is not None:
            qs1 = Product.objects.filter(title__icontains = query)
            qs2 = Product.objects.filter(description__icontains = query)
            qs3 = Product.objects.filter(price__icontains = query)
            return qs1.union(qs2, qs3)
        return Product.objects.none()

    def get_context_data(self, *args, **kwargs):
        context = super(SearchProductView, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        if len(query) < 1:
            messages.warning(self.request, "Please enter some query for search.")
        context['query'] = query
        return context

