from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone

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






def by_range(start_date, end_date=None):
    if end_date is None:
        return Order.objects.filter(updated__gte=start_date)
    return Order.objects.filter(updated__gte=start_date).filter(updated__lte=end_date)

def by_weeks_range(weeks_ago=7, number_of_weeks=2):
    if number_of_weeks > weeks_ago:
        number_of_weeks = weeks_ago
    days_ago_start = weeks_ago * 7
    days_ago_end = days_ago_start - (number_of_weeks * 7)
    start_date = timezone.now() - datetime.timedelta(days=days_ago_start)
    end_date = timezone.now() - datetime.timedelta(days=days_ago_end)
    return by_range(start_date=start_date, end_date=end_date)

def this_week_sales():
    labels = []
    data = []
    for day in range(7):
        start_date = timezone.now() - datetime.timedelta(days=1+day)
        end_date = timezone.now() - datetime.timedelta(days=day)
        qs = by_range(start_date=start_date, end_date=end_date)
        total = 0
        for i in qs:
            total += i.total
        labels.append(end_date.strftime("%A"))
        data.append(total)
    return labels, data


def sales_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            start_date = timezone.now() - datetime.timedelta(days=60)
            qs = by_range(start_date=start_date)
            this_week = by_weeks_range(weeks_ago=6, number_of_weeks=2)
            # qs = Order.objects.all()
            total = 0
            for i in qs:
                total += i.total

            this_total = 0
            for i in this_week:
                this_total += i.total

        else:
            messages.error(request, "You cannot access this page. You are not an admin user.")
            return redirect("account:account-home")
    else:
        messages.warning(request, "You cannot access this page. Please Login!")
        return redirect("account:login")
    context = {
        'all_orders': qs,
        'this_week_orders': this_week,
        'this_week_orders_total': this_total,
        'order_total': total,
    }
    return render(request, "analytics/sales.html", context=context)


def sales_ajax_view(request):
    data = {}
    if request.user.is_superuser:

        # last_week = datetime.datetime.now() - datetime.timedelta(days=7)
        # qs = Order.objects.filter(updated__gte = last_week)

        # dates = [i.updated.strftime("%A") for i in qs]
        # total_sales = [i.total for i in qs]
        labels, totals = this_week_sales()

        data['labels'] = labels[::-1] # ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        data['data'] = totals[::-1] # [random.randint(5, 500) for i in range(len(dates))]
        

    else:
        messages.warning(request, "You cannot access this page. Please Login as Admin!")
        return redirect("account:login")

    return JsonResponse(data=data)