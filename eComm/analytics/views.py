from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.http import JsonResponse

from products.models import Product
from .models import ObjectViewed
from orders.models import Order

import random
import datetime
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


def sales_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            qs = Order.objects.all()
            total = 0
            for i in qs:
                total += i.total

        else:
            messages.error(request, "You cannot access this page. You are not an admin user.")
            return redirect("account:account-home")
    else:
        messages.warning(request, "You cannot access this page. Please Login!")
        return redirect("account:login")
    context = {
        'all_orders': qs,
        'order_total': total,
    }
    return render(request, "analytics/sales.html", context=context)



def sales_ajax_view(request):
    data = {}
    if request.user.is_superuser:

        last_week = datetime.datetime.now() - datetime.timedelta(days=7)
        qs = Order.objects.filter(updated__gte = last_week)

        dates = [i.updated.strftime("%A") for i in qs]
        total_sales = [i.total for i in qs]

        data['labels'] = dates # ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        data['data'] = total_sales # [random.randint(5, 500) for i in range(len(dates))]
        

    else:
        messages.warning(request, "You cannot access this page. Please Login as Admin!")
        return redirect("account:login")

    return JsonResponse(data=data)