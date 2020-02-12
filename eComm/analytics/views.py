from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages

from products.models import Product
from .models import ObjectViewed
# Create your views here.

def user_product_history(request):
    if request.user.is_authenticated:
        c_type = ContentType.objects.get_for_model(Product)
        qs = ObjectViewed.objects.filter(content_type=c_type, user=request.user)
        test_list = [x.content_object.title[:20] for x in qs]
        print(list(set(test_list)))
        my_dict = {i:test_list.count(i) for i in test_list}
        print(my_dict)
    else:
        messages.warning(request, "You cannot access this page. Please Login!")
        return redirect("account:login")
    context = {
        "qs": qs,
    }
    return render(request, "analytics/user-product-history.html", context=context)


def product_total_views():
    c_type = ContentType.objects.get_for_model(Product)
    qs = ObjectViewed.objects.filter(content_type=c_type)
    prod_list = [x.content_object.title for x in qs]
    prod_views_dict = {i:prod_list.count(i) for i in prod_list}
    return prod_views_dict